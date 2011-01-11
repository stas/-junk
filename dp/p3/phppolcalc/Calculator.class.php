<?php
include "Divident.class.php";
include "Divider.class.php";
include "Result.class.php";

class Calculator {
    public $divident;
    public $divider;
    public $result;
    
    private $previousResult = null;
    
    function Calculator() {
        $this->divident = new Divident();
        $this->divider = new Divider();
        $this->result = new Result();
        
        $this->sum();
    }
    
    function sum() {
        $this->result->polynom = $this->divident->polynom->plus( $this->divider->polynom );
        $this->result->_print();
    }
    
    function getInstance() {
        static $instance;
        if( !is_object( $instance ) )
            $instance = new Calculator();
        
        return $instance;
    }
    
    function saveToMemento() {
        if( $this->previousResult == null )
            $this->previousResult = $this->createMemento( $this );
    }
    
    function restoreFromMemento() {
        if( $this->previousResult ) {       
            echo "Previous operations were: \n";
            $this->previousResult->divident->_print();
            $this->previousResult->divider->_print();
            $this->divident = $this->previousResult->divident;
            $this->divider = $this->previousResult->divider;
        }
    }
    
    private function createMemento( $obj ) {
        if( isset( $obj->divider ) && isset( $obj->divident ) ) {
            $m->divider = $obj->divider;
            $m->divident = $obj->divident;
            return $m;
        }
        else
            return;
    }
}
?>