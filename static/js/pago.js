var Configuration = {
  Debug: {
    Enabled: true,
    Suggestions: [
      {
        id: 1,
        name: 'Chris Evans'
      },
      {
        id: 2,
        name: 'Robert Downey Jr.'
      },
      {
        id: 3,
        name: 'Chris Hemsworth'
      },
      {
        id: 4,
        name: 'Mark Ruffalo'
      },
      {
        id: 5,
        name: 'Jeremy Renner'
      }
    ],
    PaymentInformation: {
      id: 1,
      payments: [
        {
          patient: 3,
          name: 'Language Therapy',
          observation: 'Adele',
          cost: 20.59,
          date: 11
        },
        {
          patient: 1,
          name: 'Psychotherapy',
          observation: 'Brendon',
          cost: 40.54,
          date: 14
        },
        {
          patient: 2,
          name: 'Physician Therapy',
          observation: 'Liam',
          cost: 10.54,
          date: 9
        },
        {
          patient: 3,
          name: 'Eye Therapy',
          observation: 'Kymberly',
          cost: 15.26,
          date: 12
        }
      ]
    },
    Delay: function (x) {
      return new Promise(function (resolve, reject) {
        setTimeout(function () {
          resolve(x);
        }, 2000);
      });
    }
  },
  Suggestions: {
    Limit: 5
  }
};

var State = {
  CurrentPatient: null,
  Date: {
    From: null,
    To: null
  }
}

function findMatches(q, cb) {
//     var matches, substringRegex;
//
//     // an array that will be populated with substring matches
//     matches = [];
//
//     // regex used to determine if a string contains the substring `q`
//     substrRegex = new RegExp(q, 'i');
//
//     // iterate through the pool of strings and for any string that
//     // contains the substring `q`, add it to the `matches` array
//     $.each(strs, function(i, str) {
//       if (substrRegex.test(str)) {
//         matches.push(str);
//       }
//     });
//
//     cb(matches);

  getPatientSuggestionsByNameFragment(q).then(function (suggestions) {
    cb(suggestions);
  }).bind(this);
}

$('#custom-search-input .typeahead').typeahead({
  hint: true,
  highlight: true,
  minLength: 1
},
{
  name: 'pacientes',
  display: function (data) {
    return `${data.nombres} ${data.apellidos}`
  },
  source: findMatches,
  templates: {
    empty: '<span>No existen pacientes registrados con esos nombres</span>',
    suggestion: function (data) {
      console.log(data);
      return `<div>${data.nombres} ${data.apellidos}</div>`;
    }
  }
});

$('.typeahead').bind('typeahead:select', function(ev, suggestion) {
  State.CurrentPatient = {
    Id: suggestion.id,
    Name: `${suggestion.nombres} ${suggestion.apellidos}`,
    Payments: []
  };
});
$("#datetimepicker6").on("dp.change", function (e) {
  State.Date.From = e.date;
});
$("#datetimepicker7").on("dp.change", function (e) {
  State.Date.To = e.date;
});

function generatePayments(event) {
  if (State.CurrentPatient == null) {
    alert('No hay paciente seleccionado.');
    return;
  }
  if (State.Date.From == null || State.Date.To == null) {
    alert('Los campos de fechas deben ser proveidos.');
    return;
  }
  if (State.Date.From > State.Date.To) {
    alert('La fecha de inicio debe ser previa a la de final');
    return;
  }
  $('#generate_payments_options').disabled = true;
  getPatientPaymentInformation(State.CurrentPatient.Id, {from: State.Date.From, to: State.Date.To}).then(function (payments) {
    $('#generate_payments_options').disabled = false;
  });
}

function getPatientSuggestionsByNameFragment(nameFragment) {
  var URL = API.host + '/pagos/pacientes/sugerencias?limit=' + Configuration.Suggestions.Limit || 5;
  if (nameFragment !== '') {
    URL += '&query=' + nameFragment;
  }
  return fetch(URL)
    .then(function (response) {
      if (response.ok) {
        return response.json();
      } else {
        var error = new Error(response.statusText);
        error.response = response;
        throw error;
      }
    }).then(function (json) {
      console.log(json)
      return json;
    });
}

function getPatientPaymentInformation(id, date) {
  var URL = API.host + '/pagos/pacientes/' + id + '?from=' + (date.from / 1000) + '&to=' + (date.to / 1000);
  return fetch(URL)
    .then(function (response) {
      console.log(response);
      if (response.ok) {
        return response.json();
      } else {
        var error = new Error(response.statusText);
        error.response = response;
        throw error;
      }
    })
    .then(function (payments) {
      State.CurrentPatient.Payments = payments;
      updatePatientPaymentInformationTable(payments);
    })
    .catch(function (error) {
      console.log('error');
      State.CurrentPatient.Payments = [];
      updatePatientPaymentInformationTable([]);
    });
}

function updatePatientPaymentInformationTable(payments) {
  console.log(payments);
  var tableNode = document.getElementById('patient_payments_table');
  tableNode.innerHTML = payments.map(function (payment) {
    return `<tr>
      <td>${payment.terapia_nombre}</td>
      <td>${payment.fecha_cita}, ${payment.hora_inicio} - ${payment.hora_fin}</td>
      <td>${payment.costo}</td>
    </tr>`;
  }).join('') + `<tr class="table-result">
    <td></td>
    <td>Total</td>
    <td>${payments.reduce(function (sum, payment) {
      return sum + Number(payment.costo);
    }, 0)}</td>
  </tr>`;
  var nameNode = document.getElementById('table_header_name');
  nameNode.innerHTML = State.CurrentPatient.Name;
}

var API = {
  host: 'http://localhost:8000',
  getPatientSuggestionsByNameFragment: getPatientSuggestionsByNameFragment,
  getPatientPaymentInformation: getPatientPaymentInformation
};
