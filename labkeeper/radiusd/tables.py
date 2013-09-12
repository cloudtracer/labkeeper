import django_tables2 as tables
from django_tables2.utils import A

from radiusd.models import RadiusLogin


class LoginsTable(tables.Table):
    time = tables.DateTimeColumn()
    user = tables.LinkColumn('users_profile', args=[A('user')])

    class Meta:
        model = RadiusLogin
        fields = ('time', 'user', 'device')
        empty_text = "No recent activity"
        attrs = {
            'class': 'table table-striped',
        }
