import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.util.Scanner;

public class DateClient {
    public static void main(String[] args) throws IOException {
	Scanner reader = new Scanner(System.in);
	System.out.println("\n\nEnter IP Address of desired Host that is running the date service on port 9090:");
	String serverAddress = reader.next();
        Socket s = new Socket(serverAddress, 9090);
        BufferedReader input = new BufferedReader(new InputStreamReader(s.getInputStream()));
        String answer = input.readLine();
        System.out.println("\n\nDate for the desired Host: "+serverAddress+"\n"+answer);
        System.exit(0);
    }
}
