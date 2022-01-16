int[][] sandpiles;
int TOPPLE_LIMIT = 3;

void setup() {
  size(800, 800);
  sandpiles = new int[width][height];
  sandpiles[width/2][height/2] = 1000000000;
}

void topple() {
  for (int x = 0; x < width; x++) {
    for (int y = 0; y < height; y++) {
      int current_val = sandpiles[x][y];
      if (current_val >= 4) {
        sandpiles[x][y] -= TOPPLE_LIMIT + 1;
        if (x+1 < width)
          sandpiles[x+1][y]++;
        if (x-1 >= 0)
          sandpiles[x-1][y]++;
        if (y+1 < height) 
          sandpiles[x][y+1]++;
        if (y-1 >= 0) 
          sandpiles[x][y-1]++;
      }
    }
  }
}

void render() {
  loadPixels();
  for (int x = 0; x < width; x++) {
    for (int y = 0; y < height; y++) {
      int num = sandpiles[x][y];
      color col = color(255, 0, 0);
      if (num == 0) {
        col = color(12, 64, 254);
      } else if (num == 1) {
        col = color(117, 173, 232);
      } else if (num == 2) {
        col = color(210, 184, 1);
      } else if (num == 3) {
        col = color(95, 1, 1);
      }

      pixels[x+y*width] = col;
    }
  }

  updatePixels();
} 

void draw() {
  frameRate(30);
  render(); 
  for (int i = 0; i < 100; i++) {
    topple();
  }
}
