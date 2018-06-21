package hub;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import lighting.Lighting;

public class Main extends Application {

    @Override
    public void start(Stage primaryStage) throws Exception{
        // load the splash screen which is shown when first starting and connecting to all the devices
        Parent splashRoot = FXMLLoader.load(getClass().
                getResource("Splash_fxml.fxml"));
        Scene splash = new Scene(splashRoot, 480, 320);

        // load the lighting panel
        Parent lightingRoot = FXMLLoader.load(getClass().
                getResource("../lighting/Lighting_fxml.fxml"));
        Scene lighting = new Scene(lightingRoot, 480, 320);

        // load the temperature panel
        Parent temperatureRoot = FXMLLoader.load(getClass().
                getResource("../temperature/Temperature_fxml.fxml"));
        Scene temperature = new Scene(temperatureRoot, 480, 320);

        primaryStage.setTitle("Home Automation Hub");
        primaryStage.setScene(lighting);
        primaryStage.show();
    }


    public static void main(String[] args) {
        launch(args);
    }
}
