from datetime import date, timedelta
from celery.task import Task, PeriodicTask
from celery.task.http import HttpDispatchTask
from dialer_campaign.models import *
from celery.decorators import task
from common_functions import isint
from django.db import IntegrityError
from time import sleep


@task(default_retry_delay=30 * 60)  # retry in 30 minutes.
def add(x, y):
    """This task produce the addition of 2 numbers.
    For instance (1, 2) will return '3'

    **Attributes**:

        * ``x`` -
        * ``y`` -"""

    print("Executing task id %r, args: %r kwargs: %r" % (
        add.request.id, add.request.args, add.request.kwargs))
    try:
        return x + y
    except Exception, exc:
        self.retry(exc=exc, countdown=60)  # override the default and
                                           # retry in 1 minute




@task()
def initiate_call_subscriber(subscriber_id, campaign_id):
    """This tasks will outbound the call to the subscriber

    **Attributes**:

        * ``subscriber_id`` -
        * ``callrequest_id`` -
    """
    logger = initiate_call_subscriber.get_logger()
    obj_subscriber = CampaignSubscriber.objects.get(id=subscriber_id)
    logger.info("Dialout Subscriber :: status = %s" % str(obj_subscriber.status))

    try:
        obj_campaignsubscriber = CampaignSubscriber.objects\
                                 .get(id=subscriber_id)
    except:
        logger.error('Can\'t find this CampaignSubscriber')

    try:
        obj_campaign = Campaign.objects.get(id=campaign_id)
    except:
        logger.error('Can\'t find this Campaign')


    if obj_subscriber.status == 1:
        #Here we continue
        obj_campaignsubscriber.status = 6 # Update to In Process
        obj_campaignsubscriber.save()
    else:
        logger.error("Only Pending status are processed ")
        return True

    #Check if the contact is authorized
    if not obj_campaign.is_authorized_contact(obj_campaignsubscriber.contact):
        logger.error("Contact not authorized")
        obj_campaignsubscriber.status = 7 # Update to Not Authorized
        obj_campaignsubscriber.save()
        return True

    #TODO: Spool calls to dialout

    #Construct the dialing out path
    #obj_campaign.aleg_gateway

    """
    * ``name`` - Gateway name.
        * ``description`` - Description about Gateway.
        * ``addprefix`` - Add prefix.
        * ``removeprefix`` - Remove prefix.
        * ``protocol`` - VoIP protocol
        * ``hostname`` - Hostname
        * ``secondused`` -
        * ``failover`` -
        * ``addparameter`` -
        * ``count_call`` -
        * ``count_in_use`` -
        * ``maximum_call`` -
        * ``status`` - Gateway status
    """

    #Retrieve the Gateway for the A-Leg

    #Create a Callrequest Instance to track the call task
    """**Attributes**:

            * ``uniqueid`` -
            * ``call_time`` -
            * ``exten`` -
            * ``context`` -
            * ``application`` -
            * ``timeout`` -
            * ``callerid`` -
            * ``variable`` -
            * ``account`` -
    """
    #TODO: WHAT CALLERID TO USE
    new_callrequest = Callrequest(status=1, #PENDING
                            call_time=datetime.now(),
                            timeout=30,
                            callerid='90000000',
                            phone_number=obj_campaignsubscriber.contact__contact,
                            campaign=obj_campaignsubscriber.campaign_id,
                            aleg_gateway=None,
                            voipapp=None)
    #TODO: Fix the creation of CallRequest : add all needed field
    new_callrequest.save()
    #Attach the new_callrequest.id to the call

    return True


#TODO: Put a priority on this task
@task()
def check_campaign_pendingcall(campaign_id):
    """This tasks will execute the outbound call of the campaign

    **Attributes**:

        * ``campaign_id`` -
    """
    logger = check_campaign_pendingcall.get_logger()
    logger.info("Execute the calls for the campaign = %s" % str(campaign_id))

    obj_campaign = Campaign.objects.get(id=campaign_id)

    #TODO: Control the Speed
    #if there is many task pending we should slow down
    frequency = obj_campaign.frequency # default 10 calls per minutes

    #Speed
    #check if the other tasks send for this campaign finished to be ran

    #Get the subscriber of this campaign
    # get_pending_subscriber get Max 1000 records
    list_subscriber = obj_campaign.get_pending_subscriber(frequency)
    print (list_subscriber)

    try:
        no_subscriber = list_subscriber.count()
    except AttributeError:
        no_subscriber = 0

    if no_subscriber == 0:
        logger.info("No Subscriber to proceed on this campaign")
        return False

    #find how to dispatch them in the current minutes
    time_to_wait = 60.0 / no_subscriber

    for elem_subscriber in list_subscriber:
        """Loop on Subscriber and start the initcall task"""
        initiate_call_subscriber.delay(elem_subscriber.id, campaign_id)
        sleep(time_to_wait)


class campaign_running(PeriodicTask):
    """A periodic task that check the campaign and create a tasks the calls

    **Usage**:

        campaign_running.delay()
    """
    run_every = timedelta(seconds=60)
    #run_every = timedelta(microseconds=50)

    def run(self, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info("Determine the Campaign to proceed")

        for campaign in Campaign.objects.get_running_campaign():
            logger.info("=> Campaign name %s (id:%s)" % (campaign.name,
                                                         campaign.id))

            check_campaign_pendingcall.delay(campaign.id)

        logger.info("Finish Spawn the campaign")


@task()
def collect_subscriber(campaign_id):
    """This tasks will collect all the subscriber

    **Attributes**:

        * ``campaign_id`` -
    """
    logger = collect_subscriber.get_logger()
    logger.info("Collect subscribers for the campaign = %s" % str(campaign_id))

    #Retrieve the list of active contact
    obj_campaign = Campaign.objects.get(id=campaign_id)
    list_contact = obj_campaign.get_active_contact_no_subscriber()

    if not list_contact:
        logger.info("No new contact or phonebook to import into \
        this campaign.")
        return True
    else:
        #Create CampaignSubscribers for each new active contact
        for elem_contact in list_contact:
            try:
                CampaignSubscriber.objects.create(
                                    contact=elem_contact,
                                    status=1, #START
                                    duplicate_contact=elem_contact.contact,
                                    campaign=obj_campaign)
            except IntegrityError, e:
                #We dont stop if it fails to add a suscriber to one campaign
                logger.error("IntegrityError to create CampaignSubscriber "\
                    "contact_id=%s - Error:%s" % (elem_contact.id, e))

    return True