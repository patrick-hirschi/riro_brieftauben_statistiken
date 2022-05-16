INTRO = """<!DOCTYPE html>
<html lang="en">
<head>  
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="index, follow"/>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
<script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.js" type="text/javascript" charset="utf8"></script> 
<script src="https://code.jquery.com/jquery-3.5.1.js" type="text/javascript"></script>
<script src="https://cdn.datatables.net/1.12.0/js/jquery.dataTables.min.js" type="text/javascript"></script>
<script src="https://cdn.datatables.net/buttons/2.2.3/js/dataTables.buttons.min.js" type="text/javascript"></script>
<script src="https://cdn.datatables.net/buttons/2.2.3/js/buttons.print.min.js" type="text/javascript"></script>
<script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
<script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/pdfmake.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/vfs_fonts.js"></script>
<script src="https://cdn.datatables.net/buttons/2.2.3/js/buttons.html5.min.js"></script>

<!-- Bootstrap -->
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.css">
<link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.12.0/css/jquery.dataTables.min.css">
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/buttons/2.2.3/css/buttons.dataTables.min.css">

<!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
<!-- WARNING: Respond.js doesn't work if you view the page via file:// -->

<style>
  tr td { font-size: 11px; }
  th { font-size: 12px; }
</style>
</head>
    
<body>
<div>
<h1 style="text-align: center !important; color: #4575B6 !important;">Brieftauben Altreise 2022 SG Hirschi</h1>
<p>In der nachfolgenden Tabelle sind die Leistungsdaten der Brieftauben der SG Hirschi dargestellt. Die Daten werden dazu automatisiert aus den Riro Preislisten ausgelesen und voraggregiert.</p>
<p>Für jede Taube wird die Leistung pro Flug dargestellt als <strong>"Rang bei Züchter / Rang in Gruppe / Rang in Region"</strong> und <strong>"AS-Punkte FG / AS-Punkte RV"</strong>. Ein "O" ("Härdöpfu!") bedeutet, dass die Taube zwar eingesetzt war, es allerdings nicht in die Preise geschafft hat. Nicht oder nicht mehr eingesetzte Tauben sind mit einem "-" gekennzeichnet. Die Tauben mit blauer Schrift wurden zu Beginn der Saison als die besten 5 Jährigen getippt.</p>
<p>Die Tabelle ist sortiert nach der Summe der AS-Punkte in der RV.</p>
</div>
<div>"""


OUTRO = """
</div> 
<script type="text/javascript">
    $(document).ready( function () {
    $('#result_table').DataTable( {
      "dom": 'Bfrtip',
      "buttons": [
            {
                extend: 'pdfHtml5',
                title: 'Brieftauben Altreise 2022 SG Hirschi',
                orientation: 'landscape',
                pageSize: 'LEGAL',
                stripHtml: false,
                exportOptions: { 
                  format:{ 
                    header: function(data){ 
                      var valor = data.toString();  
                      valor = valor.replace(/\<br>/g,"\\n");
                      return valor;
                    }, 
                    body: function(data){ 
                      var valor = data.toString();  
                      valor = valor.replace(/\<br>/g,"\\n");
                      return valor;
                    } 
                  } 
                }
            }
        ],
      "pageLength": 100,
      "columnDefs": [
    {"className": "dt-center", "targets": "_all"},
    {className: "no-wrap",width: "120px", targets: 0}
],"drawCallback": function () {
        $( 'tbody tr td' ).css( 'padding', '0.1px 0.1px 0.1px 0.1px' );
    }
      }).columns(-1).order('desc').draw();
    } );
</script>
</body>
</html>"""