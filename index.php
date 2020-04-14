<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
	<title>Formulário de Envio</title>
</head>

<body>
	<div class="container">
	<form action="sendmsg.php" method="post">	
		<div class="form-group">
    		<label for="exampleFormControlSelect1">Selecione o Time</label>
    		<select class="form-control" name="time">
    		<option>Flamengo</option>
    		<option>Vasco</option>
       		</select>
  		</div>
  		<div class="form-group">
    		<label for="exampleFormControlTextarea1">Texto de Envio</label>
    		<textarea class="form-control" id="exampleFormControlTextarea1" rows="3" name="texto"></textarea>
  		</div>
  		<button type="submit" class="btn btn-primary">Enviar</button>
	</form>
	</div>

</body>
</html>