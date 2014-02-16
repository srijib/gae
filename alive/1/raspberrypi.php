<?php
    $body = file_get_contents('php://input');
    $mail = new SaeMail();
    //$mail->setAttach( array( 'my_photo' => 'picture raw data' ) );
    $ret = $mail->quickSend('lihaohua90@gmail.com', 'raspberrypi initialized', $body, 'lihaohua90@gmail.com', 'snowmanshan');

    // dump info when error
    if ($ret === false)
        var_dump($mail->errno(), $mail->errmsg());

    echo "send email ok!";
?>
