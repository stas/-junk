<?php
/**
 * This is an adapter that uses Polynom interface
 */
class Result implements Polynom {
    public $polynom;
    public $resultsFileName = '/tmp/phppolcalc.log';

    function _read(){
        die( "Result can't be read.\n" );
    }
    
    function _print(){
        echo $this->polynom->toString() . "\n";
    }

    function saveLog(){
        $fh = fopen( $this->resultsFileName, 'w+' ) or die( "Can't open file." );
        fwrite( $fh, $this->polynom->toString() . "\n" );
        fclose( $fh );
    }
}
?>
