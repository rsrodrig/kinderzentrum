# -*- encoding: utf-8 -*-
from django                         import forms
from django.contrib.admin.widgets   import AdminTimeWidget
from django.forms                   import ModelForm, inlineformset_factory, BaseInlineFormSet, formset_factory, modelformset_factory
from django.forms.extras.widgets    import SelectDateWidget
from django.forms.widgets           import Widget, Select, MultiWidget
from django.utils.safestring        import mark_safe
import re
from modelos.cita_model             import Cita


time_pattern = r'(\d\d?):(\d\d)(:(\d\d))? *([aApP]\.?[mM]\.?)?$'
RE_TIME = re.compile(time_pattern)
# The following are just more readable ways to access re.matched groups:
HOURS = 0
MINUTES = 1
MERIDIEM = 4
DATEFORMAT = '%d/%m/%Y'


class SelectTimeWidget(Widget):
    """A Widget that splits time input into <select> elements.
    Allows form to show as 24hr: <hour>:<minute>."""
    hour_field = '%s_hour'
    minute_field = '%s_minute'
    meridiem_field = '%s_meridiem'    
    
    def __init__(self, attrs=None, hour_step=None, minute_step=None):
        """hour_step, minute_step are optional step values for
        for the range of values for the associated select element"""
        self.attrs = attrs or {}
        
        if hour_step: # 24hr, with stepping.
            self.hours = range(7,20,hour_step)
        else: # 24hr, no stepping
            self.hours = range(7,20) 

        if minute_step:
            self.minutes = range(0,60,15)
        else:
            self.minutes = range(0,60,15)

    def render(self, name, value, attrs=None):
        try: # try to get time values from a datetime.time object (value)
            hour_val, minute_val = value.hour, value.minute
            
        except AttributeError:
            hour_val = minute_val = 0
            if isinstance(value, basestring):
                match = RE_TIME.match(value)
                if match:
                    time_groups = match.groups();
                    hour_val = int(time_groups[HOURS]) % 24 # force to range(0-24)
                    minute_val = int(time_groups[MINUTES]) 
                                        
                    # check to see if meridiem was passed in
                    if time_groups[MERIDIEM] is not None:
                        self.meridiem_val = time_groups[MERIDIEM]                                       

        # If we're doing a 12-hr clock, there will be a meridiem value, so make sure the
        # hours get printed correctly
                    
        output = []
        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        # For times to get displayed correctly, the values MUST be converted to unicode
        # When Select builds a list of options, it checks against Unicode values
        hour_val = u"%.2d" % hour_val
        minute_val = u"%.2d" % minute_val
        
        hour_choices = [("%.2d"%i, "%.2d"%i) for i in self.hours]
        local_attrs = self.build_attrs(id=self.hour_field % id_)
        select_html = Select(attrs={'id': 'start_time', 'style': 'width:80px;margin-left: 0px'}, choices=hour_choices).render(self.hour_field % name, hour_val, local_attrs)
        output.append(select_html)

        minute_choices = [("%.2d"%i, "%.2d"%i) for i in self.minutes]
        local_attrs['id'] = self.minute_field % id_
        select_html = Select(attrs={'id': 'end_time', 'style': 'width:80px'}, choices=minute_choices).render(self.minute_field % name, minute_val, local_attrs)
        output.append(select_html)
          
        return mark_safe(u'\n'.join(output))
        

    def id_for_label(self, id_):
        return '%s_hour' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        # if there's not h:m:s data, assume zero:
        h = data.get(self.hour_field % name, 0) # hour
        m = data.get(self.minute_field % name, 0) # minute 
        
        meridiem = data.get(self.meridiem_field % name, None)
                
        if (int(h) == 0 or h) and m:
            return '%s:%s' % (h, m)

        return data.get(name, None)

        
class CitaForm(ModelForm):
    required_css_class = 'required'
    #error_css_class = 'has-error'
    class Meta:
        model = Cita
        fields = ['fecha_cita',
                  'hora_inicio',
                  'hora_fin',                                    
                  'tipo_terapia',
                  'paciente',
                  'terapista',
                  'estado',
                  'indicaciones']
        widgets = {'fecha_cita': forms.DateInput(attrs= {'class':'datepicker form-control', 'placeholder': 'Hacer click aquí para desplegar el calendario'}, format=DATEFORMAT),
                   'hora_inicio': SelectTimeWidget(),
                   'hora_fin': SelectTimeWidget(),                   
                   'tipo_terapia': forms.Select(attrs={'class':'form-control'}),
                   'paciente': forms.Select(attrs={'class':'form-control'}),
                   'terapista': forms.Select(attrs={'class':'form-control'}),
                   'estado': forms.Select(attrs={'class':'form-control'} ),                    
                   'indicaciones':forms.TextInput(attrs={'value':'pendientes'})
                   }   