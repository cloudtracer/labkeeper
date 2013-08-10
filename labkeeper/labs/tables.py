import django_tables2 as tables
from labs.models import Membership


class MembershipTable(tables.Table):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False)
    user = tables.Column(verbose_name='Member')
    joined = tables.DateColumn(format="Y-m-d")

    class Meta:
        model = Membership
        fields = ('selection', 'user', 'joined', 'role')
        attrs = {
            'class': 'table table-striped',
        }