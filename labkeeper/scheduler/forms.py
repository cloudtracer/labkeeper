from datetime import timedelta
from dateutil import parser

from django import forms
from django.db.models import Q
from django.utils import timezone


class ReservationForm(forms.Form):

    class Meta:
        pass

    def __init__(self, lab, schedule, tz, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)

        self.lab = lab
        self.schedule = schedule
        self.tz = tz

        # Allow multi-pod Reservations?
        if lab.allow_multipod:
            self.fields['pods'] = forms.MultipleChoiceField(choices=[(p.id, p.name) for p in lab.pods.all()], widget=forms.CheckboxSelectMultiple)
        else:
            self.fields['pods'] = forms.ChoiceField(choices=[(p.id, p.name) for p in lab.pods.all()])

        # Starting date
        self.fields['date'] = forms.ChoiceField(choices=[(d, d.strftime("%b %-d (%a)")) for d in schedule.get_days()])

        # Starting time
        self.fields['time'] = forms.ChoiceField(choices=[(h.strftime("%H:%M"), h.strftime("%H:%M")) for h in lab.get_open_hours(tz=tz)])

        # Duration (in hours)
        self.fields['duration'] = forms.ChoiceField(choices=[(x, " {0} hours".format(x)) for x in range(lab.min_reservation, lab.max_reservation+1)])

    def clean(self):
        cleaned_data = super(ReservationForm, self).clean()

        # We can't check for Reservation conflicts if the form isn't valid to begin with.
        if self._errors:
            return cleaned_data

        # Calculate start and end times of the requested time slot
        start_time = self.tz.localize(parser.parse(cleaned_data['date'] + ' ' + cleaned_data['time']))
        end_time = start_time + timedelta(hours=int(cleaned_data['duration'])) - timedelta(minutes=1)

        # Verify that end_time is in the future
        if end_time <= timezone.now():
            raise forms.ValidationError("You cannot make a reservation in the past.")

        # Verify the Reservation falls within the Lab's open hours
        if end_time.hour not in [h.hour for h in self.lab.get_open_hours(self.tz)]:
            self._errors['duration'] = self.error_class(["You can only reserve time during which the lab is open."])

        # Verify this Reservation does not conflict with another
        #  - Listify Pod ID(s) as integers
        if isinstance(cleaned_data['pods'], list):
            pod_ids = [int(id) for id in cleaned_data['pods']]
        else:
            pod_ids = [int(cleaned_data['pods'])]
        # - Find all Reservations which overlap with the requested time slot
        overlaps = self.lab.reservations.filter(
            Q(start_time__range=(start_time, end_time)) |
            Q(end_time__range=(start_time, end_time)) |
            Q(start_time__lt=start_time, end_time__gte=end_time)
        )
        #  - Raise an error on the first overlapping Reservation with a common Pod
        for overlap in overlaps:
            for pod in overlap.pods.all():
                if pod.id in pod_ids:
                    raise forms.ValidationError("Your requested time slot conflicts with an existing reservation: Pod {0} reserved at {1}".format(pod, overlap.start_time.astimezone(self.tz).time()))

        return cleaned_data
