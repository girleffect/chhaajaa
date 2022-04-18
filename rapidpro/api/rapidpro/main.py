from api.rapidpro.requests.rpp_ftbl_contact import Contacts
from api.rapidpro.requests.fields import Fields
from api.rapidpro.requests.rpp_ftbl_flows_flow_label import FlowLabel
from api.rapidpro.requests.rpp_ftbl_flows_flow import Flows
from api.rapidpro.requests.rpp_ftbl_flows_flowstart import FlowStart
from api.rapidpro.requests.rpp_ftbl_flows_flowrun import Runs
from api.rapidpro.requests.rpp_ftbl_msgs_msg import Messages
from api.rapidpro.requests.rpp_ftbl_msgs_broadcast_urns import BroadcastUrls
from api.rapidpro.requests.rpp_ftbl_auth_user import AuthUser
from api.rapidpro.requests.rpp_ftbl_contacts_contactgroupcount import ContactGroupCount


from . import session


class pyRapid:
    """ """

    rpp_ftbl_contact = Contacts(session)
    fields = Fields(session)
    rpp_ftbl_flows_flow_label = FlowLabel(session)
    rpp_ftbl_flows_flow = Flows(session)
    rpp_ftbl_flows_flowstart = FlowStart(session)
    rpp_ftbl_flows_flowrun = Runs(session)
    rpp_ftbl_msgs_msg = Messages(session)
    rpp_ftbl_msgs_broadcast_urns = BroadcastUrls(session)
    rpp_ftbl_auth_user = AuthUser(session)
    rpp_ftbl_contacts_contactgroupcount = ContactGroupCount(session)
