import java.io.*;

public class TestFileStream {
    public static void main(String[] args) throws IOException {
        try (
            FileOutputStream output = new FileOutputStream("temp.dat");
        ) {
            for (int i = 1; i <= 10; i++) {
                output.write(i);
            }
        }

        try (
            // Create an input stream for the file
            FileInputStream input = new FileInputStream("temp.dat");
        ) {
            // Read values from the file
            int value;
            while ((value = input.read()) != -1) {
                System.out.print(value + " ");
            }
        }
    }
}