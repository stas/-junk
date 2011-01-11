/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package javapolcalc;

/**
 * Result class that uses Polynom interface
 * @author stas
 */
public class Result implements Polynom {
    Polynomial polynom;

    public void read() {
        throw new UnsupportedOperationException("Result can't be read.");
    }

    public void print() {
        System.out.println( this.polynom.toString() );
    }
}
