print 'Content-Type: text/html; charset=utf-8'
print ''
print '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Arook Web Proxy For Google App Engine</title>
<style type="text/css">
body,input{font-size:24px;}
</style>
<script type="text/javascript">
function go(f)
{
	location.href = '/' + f.url.value;
	return false;
}
</script>
</head>

<body>
Overall Proxy For Google App Engine<br />
<form onsubmit="return go(this)">
http://<input type="text" name="url" id="url" size="40" />
<input type="submit" value="go"/>
</form>
</body>
</html>'''
