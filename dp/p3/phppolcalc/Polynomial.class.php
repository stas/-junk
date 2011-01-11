<?php
class Polynomial {
    public $coef;
    public $deg;
    
    function Polynomial( $a, $b ) {
        $this->coef[intval($b)] = intval($a);
        $this->deg = $this->degree();
    }
    
    function degree() {
        $d = 0;
        if( count( $this->coef ) == 1 ) {
            $d = reset( array_keys( $this->coef ) );
            return $d;
        } elseif( count( $this->coef ) > 1 ) {
            $keys = array_keys( $this->coef );
            sort( $keys );
            $d = end( $keys );
            return $d;
        } else
            return $d;
    }
    
    function plus( $second ) {
        $first = $this;
        $result = new Polynomial( 0, max( $this->deg, $second->deg ) );
        for( $i = 0; $i <= $first->deg; $i++ )
            if( isset( $first->coef[$i] ) ) {
                if( !isset( $result->coef[$i] ) )
                    $result->coef[$i] = 0;
                $result->coef[$i] += $first->coef[$i];
            }
        for( $i = 0; $i <= $second->deg; $i++ )
            if( isset( $second->coef[$i] ) ) {
                if( !isset( $result->coef[$i] ) )
                    $result->coef[$i] = 0;
                $result->coef[$i] += $second->coef[$i];
            }
        
        $result->deg = $result->degree();
        return $result;
    }
    
    function toString() {
        if( $this->deg == 0 )
            return "" . $this->coef[0];
        
        if( $this->deg == 1 )
            return $this->coef[1] . "x";
        
        $s = $this->coef[$this->deg] . "x^" . $this->deg;
        for( $i = $this->deg - 1; $i >= 0; $i-- ) {
            if( !isset( $this->coef[$i] ) || $this->coef[$i] == 0 )
                continue;
            elseif( $this->coef[$i] > 0 )
                $s .= "+" . $this->coef[$i];
            elseif( $this->coef[$i] < 0 )
                $s .= "-" . -$this->coef[$i];
            
            if( $i == 1 )
                $s .= "x";
            elseif( $i > 1 )
                $s .= "x^" . $i;
        }
        return $s;
    }
}
?>