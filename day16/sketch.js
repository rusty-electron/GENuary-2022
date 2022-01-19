angle_x = 45;
angle_y = 0;

function setup() {
  createCanvas(600, 600, WEBGL); // create a webgl canvas
}

function draw() {
  background(51);
  rectMode(CENTER);

  // create three point lights
  pointLight(230, 57, 70, -2000, 0, 10);
  pointLight(29, 53, 87, 0, 2000, 10);
  pointLight(189, 247, 183, 0, -2000, 10);

  noStroke();
  fill(255, 0, 150);

  // use ambient material
  ambientMaterial(255);

  // increment angle slowly
  angle_x += 0.02;
  angle_y -= 0.03;

  // rotate and draw shapes
  rotateX(angle_x);
  rotateY(angle_y);
  torus(120, 40)

  rotateX(-angle_x);
  rotateY(-angle_y);
  box(50, 50);

  box(1000, 1000, 1000)
}
