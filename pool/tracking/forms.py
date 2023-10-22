from django import forms


class ScanForm(forms.Form):
    scann = forms.CharField(max_length=100, label="scan")