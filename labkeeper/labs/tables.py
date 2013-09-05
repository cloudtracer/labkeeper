import django_tables2 as tables
from django_tables2.utils import A

from django.utils.safestring import mark_safe

from labs.models import Device, Membership


DEVICE_ACTIONS = """
<a href="{% url 'labs_edit_device' record.id %}">edit</a> |
<a href="{% url 'labs_delete_device' record.id %}" class="text-error" onclick="return confirm('Delete device {{ record.name }}?')">delete</a>
"""


class DeviceManagementTable(tables.Table):
    name = tables.LinkColumn('labs_edit_device', args=[A('pk')])
    cs = tables.Column(accessor='cs_port.consoleserver', verbose_name='Console Server')
    cs_port = tables.Column(verbose_name='Port', accessor='cs_port.number')
    actions = tables.TemplateColumn(DEVICE_ACTIONS, orderable=False)

    class Meta:
        model = Device
        fields = ('name', 'pod', 'type', 'cs', 'cs_port', 'description', 'actions')
        empty_text = "No devices yet"
        attrs = {
            'class': 'table table-striped',
        }


class MembershipTable(tables.Table):
    user = tables.LinkColumn('users_profile', args=[A('user')])
    joined = tables.DateColumn(format="Y-m-d")

    class Meta:
        model = Membership
        fields = ('user', 'joined', 'role')
        attrs = {
            'class': 'table table-striped',
        }


class MembershipManagementTable(MembershipTable):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False)

    class Meta(MembershipTable.Meta):
        fields = ('selection',)
