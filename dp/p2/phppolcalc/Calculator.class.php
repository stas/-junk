<?php
include "CalculatorDecorator.class.php";

class Calculator extends CalculatorDecorator {
    public $result;
    
    function Calculator() {
        $this->divident = new Divident();
        $this->divider = new Divider();
        $this->result = new Result();
        $this->sum();
    }
    
    function sum() {
        $this->result->polynom = $this->divident->polynom->plus( $this->divider->polynom );
        $this->result->_print();
        $this->result->saveLog();
    }
    
    function printOperators() {}
}
?>