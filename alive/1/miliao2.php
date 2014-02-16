<?php
function GetSignature($queryString)
{
    $salt = "8007236f-a2d6-4847-ac83-c49395ad6d65";
    $result = $queryString."&".$salt;
    return md5(base64_encode($result));
}
function GetNewAccount()
{
    $ch=curl_init();
    $api26 = "http://api.chat.xiaomi.net/v2/user/put";
    $user = rand(100000, 999999);
    $qString = 'nickname='.$user.'&pwd='.md5($user);
    curl_setopt_array(
        $ch,
        array(
            CURLOPT_URL=>$api26."?s=".GetSignature($qString),
            CURLOPT_RETURNTRANSFER=>true,
            CURLOPT_POST=>true,
            CURLOPT_POSTFIELDS=>$qString,
        )
    );
    $content=curl_exec($ch);
    if(curl_errno($ch)) $result = curl_error($ch);
    else $result = $content;
    curl_close($ch);
    return "nick and pwd: ".$user.", result: ".$result;
}
if (!isset($_REQUEST['n']) || !isset($_REQUEST['key']) || $_REQUEST['key'] != '2013BetterMiliao') die('die.');
$count = intval($_REQUEST['n']);
$max = 25;
if ($count > $max)
{
    $count = $max;
    echo "Max count: ". $max . '<br>';
}
for ($i = 0; $i < $count; $i++)
{
    echo GetNewAccount() . "<br>";
}
?>

