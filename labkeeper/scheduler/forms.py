from django import forms


class ReservationForm(forms.Form):

    class Meta:
        pass

    def __init__(self, lab, schedule, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)

        # Allow multi-pod Reservations?
        if lab.allow_multipod:
            self.fields['pods'] = forms.MultipleChoiceField(choices=[(p.id, p.name) for p in lab.pods.all()], widget=forms.CheckboxSelectMultiple)
        else:
            self.fields['pods'] = forms.ChoiceField(choices=[(p.id, p.name) for p in lab.pods.all()])

        # Date
        self.fields['date'] = forms.ChoiceField(choices=[(d, d.strftime("%b %-d (%a)")) for d in schedule.get_days()])

        # Starting time
        self.fields['time'] = forms.ChoiceField(choices=[(h, h) for h in schedule.get_hours()])

        # Duration (in hours)
        self.fields['duration'] = forms.ChoiceField(choices=[(x, " {0} hours".format(x)) for x in range(lab.min_reservation, lab.max_reservation+1)])