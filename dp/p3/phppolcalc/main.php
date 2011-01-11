#!/usr/bin/env php
<?php
include "Calculator.class.php";

$calculator = new Calculator();
$calculator->saveToMemento();
$calculator->restoreFromMemento();
$calculator->sum();
?>