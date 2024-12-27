from django import forms
from .models import Cliente, Servicio, Presupuesto, ItemPresupuesto
#Presupuestos
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, HTML


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono', 'empresa']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border rounded'}),
            'telefono': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded'}),
            'empresa': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded'})
        }


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'precio_unitario']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'descripcion': forms.Textarea(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline h-24'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'step': '0.01'})
        }

class ItemPresupuestoForm(forms.ModelForm):
    class Meta:
        servicio = forms.ModelChoiceField(
        queryset=Servicio.objects.all(),
        widget=forms.Select(attrs={
            'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
        })
    )

    class Meta:
        model = ItemPresupuesto
        fields = ['servicio']

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['cliente', 'fecha_validez', 'notas']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'fecha_validez': forms.DateInput(attrs={'type': 'date', 'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'notas': forms.Textarea(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'rows': 3})

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('cliente', css_class='w-full'),
                Column('fecha_validez', css_class='w-full'),
            ),
            'notas',
            HTML('<div id="items-container">{% include "presupuestos/items_form.html" %}</div>'),
            HTML('<button type="button" id="add-item" class="bg-green-500 text-white px-4 py-2 rounded mt-2">Agregar Ítem</button>'),
            Submit('submit', 'Guardar Presupuesto', css_class='bg-primary text-white px-4 py-2 rounded mt-4')
        )