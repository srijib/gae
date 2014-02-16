<?php

$kv = new SaeKV();
$ret = $kv->init();

$new_ip = $_SERVER['REMOTE_ADDR'];
  
function update_state(&$kv, $new_ip)
{
  // $keys = array('HTTP_X_FORWARDED_FOR', 'HTTP_X_REAL_IP', 'REMOTE_ADDR');

  /*
  foreach ($keys as &$key)
  {
      $value =  $_SERVER[$key];
      $results[$key] = $value;
      // echo $key . ": ". $value . "\n";
  }
  */
  
  // $json = json_encode($results);
  /*
  $ret = $kv->set('ddns', $json);
  $ret = $kv->set('remote_ip', $results['REMOTE_ADDR']);
  $ret = $kv->set('ddns_time', date(DATE_RFC822));  
  */
  
  $ret = $kv->set('remote_ip', $new_ip);
  $ret = $kv->set('update_time', date(DATE_RFC822));
  return $new_ip;
}

if (isset($_REQUEST['post']))
{
  $new_ip = update_state($kv, $new_ip);
  echo $new_ip;
}
else if (isset($_REQUEST['check']))
{
  $previous_ip = $kv->get('remote_ip');
  $last_update_time = $kv->get('last_update_time');
  if ($previous_ip != $new_ip)
  {
    $new_ip = update_state($kv, $new_ip);
    echo "changed";
  }
  else echo "no change";
  
  echo "\n" . $new_ip . "\n" . $last_update_time;
}
else if (isset($_REQUEST['updated']))
{
  $update_time = time();
  $kv->set('last_update_time', $update_time);
  echo $update_time;
}
else
{
  $previous_ip = $kv->get('remote_ip');
  $time = $kv->get('update_time');
  echo $time . "<br>" . $previous_ip;
}

?>
