import java.io.*;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Date;
import com.pi4j.io.gpio.GpioController;
import com.pi4j.io.gpio.GpioFactory;
import com.pi4j.io.gpio.GpioPinDigitalOutput;
import com.pi4j.io.gpio.PinState;
import com.pi4j.io.gpio.RaspiPin;

public class DateServer {
    public static void main(String[] args) throws IOException, InterruptedException {
	final GpioController gpio = GpioFactory.getInstance();	
	//GPIO Pin 5 as Yellow LED position
	final GpioPinDigitalOutput pin = gpio.provisionDigitalOutputPin(RaspiPin.GPIO_05, "MyLED", PinState.LOW);
	pin.setShutdownOptions(true, PinState.LOW);

        ServerSocket listener = new ServerSocket(9090);
        try {
            while (true) {
                Socket socket = listener.accept();
                try {
                    PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                    out.println(new Date().toString());
		    pin.high();
        	    System.out.println("\n\nYellow LED turn on indicating Date of desired host has been displayed.\n\n");
        	    gpio.shutdown();

                } finally {
                    socket.close();
                }
            }
        }
        finally {
            listener.close();
        }
    }
}
