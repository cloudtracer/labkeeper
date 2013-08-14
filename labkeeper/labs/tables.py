import django_tables2 as tables

from django.utils.safestring import mark_safe

from labs.models import Membership


class MembershipTable(tables.Table):
    user = tables.Column(verbose_name='Member')
    joined = tables.DateColumn(format="Y-m-d")

    class Meta:
        model = Membership
        fields = ('user', 'joined', 'role')
        attrs = {
            'class': 'table table-striped',
        }

    def render_user(self, value):
        return mark_safe("<a href=\"{0}\">{1}</a>".format(value.get_absolute_url(), value))


class MembershipManagementTable(MembershipTable):
    selection = tables.CheckBoxColumn(accessor="pk", orderable=False)

    class Meta(MembershipTable.Meta):
        fields = ('selection', 'user', 'joined', 'role')
