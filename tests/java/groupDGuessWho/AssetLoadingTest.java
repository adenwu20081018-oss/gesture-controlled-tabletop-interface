package groupDGuessWho;

import java.awt.*;
import java.nio.file.*;
import javax.swing.*;
import javax.imageio.ImageIO;
import javax.sound.sampled.AudioSystem;

/** Checks filesystem resources and real game screens after asset moves. */
public final class AssetLoadingTest {
    private static int images, audio, icons;
    private static Object field(Board board, String name) throws Exception {
        var f = Board.class.getDeclaredField(name); f.setAccessible(true); return f.get(board);
    }
    private static void inspect(Component component) {
        Icon icon = component instanceof AbstractButton b ? b.getIcon()
                : component instanceof JLabel l ? l.getIcon() : null;
        if (icon != null) {
            if (icon.getIconWidth() <= 0 || icon.getIconHeight() <= 0)
                throw new AssertionError("Unloaded icon: " + icon);
            icons++;
        }
        if (component instanceof Container c)
            for (Component child : c.getComponents()) inspect(child);
    }
    @SuppressWarnings("unchecked")
    public static void main(String[] args) throws Exception {
        try (var paths = Files.walk(Path.of("assets"))) {
            for (Path p : paths.filter(Files::isRegularFile).toList()) {
                if (p.toString().endsWith(".png")) {
                    if (ImageIO.read(p.toFile()) == null) throw new AssertionError(p);
                    images++;
                } else if (p.toString().endsWith(".wav")) {
                    try (var stream = AudioSystem.getAudioInputStream(p.toFile())) {
                        if (stream.read(new byte[64]) <= 0) throw new AssertionError(p);
                    }
                    audio++;
                }
            }
        }
        SwingUtilities.invokeAndWait(() -> {
            Board board = null;
            try {
                board = new Board();
                inspect(board.controlWindow());
                JButton start = (JButton) field(board, "startGame");
                for (int i = 0; i < 5; i++) { start.doClick(0); inspect(board.controlWindow()); }
                var characters = (java.util.List<Character1>) field(board, "charactersOnScreen");
                Character1 original = characters.get(0);
                try (var paths = Files.list(Path.of("assets/characters"))) {
                    for (Path p : paths.filter(p -> p.getFileName().toString().matches("[A-Z]{2}[0-9]{2}\\.png")).toList()) {
                        String id = p.getFileName().toString().replace(".png", "");
                        characters.set(0, new Character1(id,"","","",false,false,false,false,false));
                        for (String variant : new String[]{"default","exclude","target"}) {
                            board.setUpImage(0, variant); inspect(board.controlWindow());
                            String expected = "assets/characters/" + id + (variant.equals("default") ? "" : variant) + ".png";
                            if (!((JButton[])field(board,"characterDisplay"))[0].getIcon().toString().equals(expected))
                                throw new AssertionError("Wrong portrait: " + expected);
                        }
                    }
                }
                characters.set(0, original);
                board.resultMenuOn(true); inspect(board.controlWindow());
                board.resultMenuOn(false); inspect(board.controlWindow());
                board.mainMenuOn(); inspect(board.controlWindow());
            } catch (Exception e) { throw new RuntimeException(e); }
            finally { if (board != null) { board.play.stopMusic(); board.controlWindow().dispose(); } }
        });
        System.out.println("Asset checks passed: " + images + " PNGs, " + audio + " WAVs; " + icons + " screen icon checks.");
    }
}
