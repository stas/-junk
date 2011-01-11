/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package javapolcalc;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

/**
 * Result Adapter that uses Polynom interface
 * @author stas
 */
public class Result implements Polynom {
    Polynomial polynom;
    String resultsFileName = "/tmp/javapolcalc.log";

    public void read() {
        throw new UnsupportedOperationException("Result can't be read.");
    }

    public void print() {
        System.out.println( this.polynom.toString() );
    }

    public void saveLog() throws IOException {
        BufferedWriter log = new BufferedWriter( new FileWriter( resultsFileName, true ) );
        log.append( this.polynom.toString() );
        log.newLine();
        log.close();
        System.out.println( "Results saved in " + resultsFileName + "\n" );
    }
}
