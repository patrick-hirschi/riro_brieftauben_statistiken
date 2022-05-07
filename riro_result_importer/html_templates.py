INTRO = """<!DOCTYPE html>
<html lang="en">
<head>  
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="index, follow"/>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
<!-- Bootstrap -->
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.css">
<link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
<script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.js"></script> 
<!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
<!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
<script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
<script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
</head>
    
<body>
<div>
<h1>Brieftauben Altreise 2022 SG Hirschi</h1>
<p>In der nachfolgenden Tabelle sind die Leistungsdaten der Brieftauben der SG Hirschi dargestellt. Die Daten werden dazu automatisiert aus den Riro Preislisten ausgelesen und voraggregiert. Für jede Taube wird die Leistung pro Flug dargestellt als <strong>"Rang in Gruppe / Rang in Region"</strong> und <strong>"AS-Punkte FG / AS-Punkte RV"</strong>.</p>
<p>Die Tabelle ist sortiert nach der Summer der AS-Punkte in der RV.</p>
</div>
<div>"""


OUTRO = """
</div> 
<script type="text/javascript">
    $(document).ready( function () {
    $('#result_table').DataTable( {
      "pageLength": 100,
      "columnDefs": [
    {"className": "dt-center", "targets": "_all"}
],"drawCallback": function () {
        $( 'tbody tr td' ).css( 'padding', '1px 1px 1px 1px' );
    }
      }).columns(-1).order('desc').draw();
    } );
</script>
</body>
</html>"""