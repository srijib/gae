<?php

function doRun(&$strCode, &$show_status, &$content_type){
    switch($content_type){
    case 'plain':
        header("Content-Type: text/plain; charset=UTF-8");
        break;
    case 'html':
        header("Content-Type: text/html; charset=UTF-8");
        break;
    default:
        break;
    }
    $start_time = microtime(true);
    eval($strCode);
    $delta_time = microtime(true) - $start_time;
    if(!$show_status) return;
    echo "\n";
    echo "Code costs ".$delta_time." seconds.\n";
    echo "Current memory usage: ". memory_get_usage()/1024 ." KB.\n";
    echo "Current memory peak usage: ". memory_get_peak_usage()/1024 ." KB.\n";
}

function doSave(&$strCode, &$filename){
    $PRE = "codes";
    if(!is_dir($PRE)) mkdir($PRE);
    $full_path = $PRE.'/'.$filename;
    if(file_exists($full_path)) die('error: file already existed, you may not want to overwrite it.');
    file_put_contents($full_path, $strCode);
    echo $full_path." saved.\n";
}

if (isset($_POST['code'])) {
    $strCode = $_POST['code'];
    if(empty($strCode)) die('error: Please input some code.');
    if(empty($_REQUEST['action'])) die('error: No action given.');
    $action = $_REQUEST['action'];
    switch($action){
    case 'run':
        if(empty($_REQUEST['status'])) $show_status = false; else $show_status = true;
        if(isset($_REQUEST['contenttype'])) $content_type = $_REQUEST['contenttype']; else $content_type = '';
        doRun($strCode, $show_status, $content_type);
        break;
    case 'save':
        if(empty($_REQUEST['filename'])) die('error: No filename given.');
        $filename = $_REQUEST['filename'];
        doSave($strCode, $filename);
        break;
    default:
        die('error: action not supported.');
    }
}
else{
    header("Content-Type: text/html; charset=UTF-8");
    echo <<<EOF
<h2>PHP playground</h2>
<form action="sh.php" method="post" target="result">
<textarea name="code" style="width:100%;height:150px;"></textarea><br/>
<input type="radio" name="action" value="run" checked="true" />运行
<input type="checkbox" name="status" checked="true" />显示运行时统计
<input type="radio" name="contenttype" value="null" />不指定header
<input type="radio" name="contenttype" checked="true" value="plain" />以text/plain,utf-8形式输出
<input type="radio" name="contenttype" value="html" />以text/html,utf-8形式输出<br/>
<input type="radio" name="action" value="save" />保存
文件名:<input type="text" name="filename" value="" />
<input type="submit" value="提交" />
</form>
<iframe name="result" style="width:100%;height:400px;"></iframe>
EOF;
}
?>
