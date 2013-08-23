import django_tables2 as tables
from django_tables2.utils import A

from django.utils.safestring import mark_safe

from scheduler.models import Reservation


class ReservationTable(tables.Table):

    id = tables.LinkColumn('scheduler_reservation', args=[A('pk')])
    start_time = tables.DateTimeColumn()
    lab = tables.LinkColumn('labs_lab', args=[A('lab.id')])
    get_pods = tables.TemplateColumn('{{ value|join:", "}}', verbose_name='Pods')
    duration = tables.TemplateColumn('{{ value }} hour{{ value|pluralize }}', verbose_name='Duration')

    class Meta:
        model = Reservation
        fields = ('id', 'start_time', 'time_until', 'lab', 'get_pods', 'duration', 'created_time')
        empty_text = "Nothing scheduled"
        attrs = {
            'class': 'table table-striped',
        }