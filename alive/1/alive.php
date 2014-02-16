<?php
echo '<strong>Welcome to SAE!</strong>';
function sendmail(){
  $mail = new SaeMail();
  //$mail->setAttach( array( 'my_photo' => '照片的二进制数据' ) );
  //$ret = $mail->quickSend( 'to@sina.cn' , '邮件标题' , '邮件内容' , 'smtpaccount@gmail.com' , 'password' );
  $ret = $mail->quickSend( 'egg90@sina.cn', 'try' , 'try' , 'egg90@sina.cn' , 'Lihaohuaasdf' );
  //发送失败时输出错误码和错误信息
  if ($ret === false)
      var_dump($mail->errno(), $mail->errmsg());
  echo "发送成功";
}
sendmail();
?>

