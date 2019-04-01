//
// Use multiple 8x8 dot matrix modules to display a marquee string
// http://www.icshop.com.tw/product_info.php/products_id/13181
//
// MAX7219 datasheet: https://datasheets.maximintegrated.com/en/ds/MAX7219-MAX7221.pdf
//

#define Tx 51
#define Rx 50

#include <SoftwareSerial.h>
SoftwareSerial BT(Rx, Tx);

String s;
String dis = "2019 makentu! let's go pikachu";

// the MAX7219 address map (datasheet table 2)
#define MAX7219_DECODE_REG      (0x09)
#define MAX7219_INTENSITY_REG   (0x0A)
#define MAX7219_SCANLIMIT_REG   (0x0B)
#define MAX7219_SHUTDOWN_REG    (0X0C)
#define MAX7219_DISPLAYTEST_REG (0x0F)
#define MAX7219_COLUMN_REG(pos) ((pos) + 1)

// shutdown mode (datasheet table 3)
#define MAX7219_OFF             (0x0)
#define MAX7219_ON              (0x1)

const int clock_pin = 35;
const int data_latch_pin = 33;
const int data_input_pin = 31;
const int sensor_pin = 45;
const int IN3 = 38;
const int IN4 = 39;
const int MH = 32;
const int SN1 = 22;
const int SN2 = 23;
const int SN3 = 24;
const int SN4 = 25;

bool pressed = false;

// number of columns of the display matrx
#define NUM_OF_COLUMNS  (8)

// define the number of chained matrixes
#define NUM_OF_MATRIXES (3)

// matrix pattern for "Hi!"
const byte char_pattern[][6] =
{
  {B00000000, B01111100, B00010010, B01111100, B00000000},//01 A
  {B00000000, B01111110, B01011010, B00110100, B00000000},//02 B
  {B00000000, B00111100, B01100110, B01000010, B00000000},//03 C
  {B00000000, B01111110, B01000010, B00111100, B00000000},//04 D
  {B00000000, B01111110, B01001010, B01001010, B00000000},//05 E
  {B00000000, B01111110, B00001010, B00001010, B00000000},//06 F
  {B00111100, B01000010, B01010010, B00110010, B01110000},//07 G
  {B00000000, B01111110, B00010000, B01111110, B00000000},//08 H
  {B00000000, B01000010, B01111110, B01000010, B00000000},//09 I
  {B00000000, B01000010, B01111110, B00000010, B00000000},//10 J
  {B00000000, B01111110, B00001000, B01110110, B00000000},//11 K
  {B00000000, B01111110, B01000000, B01000000, B00000000},//12 L
  {B01111110, B00000100, B01111000, B00000100, B01111110},//13 M
  {B01111110, B00000100, B00011000, B00100000, B01111110},//14 N
  {B00000000, B00111100, B01000010, B00111100, B00000000},//15 O
  {B00000000, B01111110, B00010010, B00001100, B00000000},//16 P
  {B00111100, B01010010, B01100010, B00111100, B01100000},//17 Q
  {B00000000, B01111110, B00010010, B01101100, B00000000},//18 R
  {B00000000, B00100100, B01001010, B00110100, B00000000},//19 S
  {B00000000, B00000010, B01111110, B00000010, B00000000},//20 T
  {B00000000, B01111110, B01000000, B01111110, B00000000},//21 U
  {B00000000, B00111110, B01000000, B00111110, B00000000},//22 V
  {B00111110, B01000000, B00110000, B01000000, B00111110},//23 W
  {B00000000, B01110110, B00001000, B01110110, B00000000},//24 X
  {B00000000, B00001110, B01111000, B00001110, B00000000},//25 Y
  {B00000000, B01101010, B01011010, B01010110, B00000000},//26 Z
  {B00000000, B00000000, B00000000, B00000000, B00000000},//27  
  {B00000000, B00000100, B01010010, B00001100, B00000000},//28 ?
  {B00000000, B00000000, B01011110, B00000000, B00000000},//29 !
  {B01111110, B01000010, B01011010, B01111110, B00000000},//30 0
  {B00000000, B01000100, B01111110, B01000000, B00000000},//31 1
  {B00000000, B01100100, B01010010, B01001100, B00000000},//32 2
  {B00000000, B01001010, B01001010, B01111110, B00000000},//33 3 
  {B00010000, B00011000, B00010100, B01111110, B00010000},//34 4
  {B00000000, B01101110, B01001010, B01111010, B00000000},//35 5
  {B00000000, B01111110, B01010010, B01110110, B00000000},//36 6
  {B00000000, B00000110, B00000010, B01111110, B00000000},//37 7
  {B00111000, B01101110, B01001010, B01101110, B00111000},//38 8
  {B00000000, B01101110, B01001010, B01111110, B00000000},//39 9
  {B00000000, B00010110, B00001110, B00000000, B00000000}//40 '
};
const byte blank_pattern[] =
{
  B00000000
};

#define DISPLAY_COLUMN_LENGTH (sizeof(char_pattern[0]))
#define DISPLAY_FRAMES (sizeof(char_pattern)/sizeof(char_pattern[0]))

// update a specific register value of all MAX7219s
void set_all_registers(byte address, byte value)
{
  digitalWrite(data_latch_pin, LOW);

  for (int i = 0; i < NUM_OF_MATRIXES; i++)
  {
    shiftOut(data_input_pin, clock_pin, MSBFIRST, address);
    shiftOut(data_input_pin, clock_pin, MSBFIRST, value);
  }
  
  digitalWrite(data_latch_pin, HIGH);
}

void clear_all_matrix()
{
  // clear the dot matrix
  for (int i = 0; i < NUM_OF_COLUMNS; i++)
  {
    set_all_registers(MAX7219_COLUMN_REG(i), B00000000);
  }
}

void init_all_max7219()
{
  // disable test mode. datasheet table 10
  set_all_registers(MAX7219_DISPLAYTEST_REG, MAX7219_OFF);
  // set medium intensity. datasheet table 7
  set_all_registers(MAX7219_INTENSITY_REG, 0x1);
  // turn off display. datasheet table 3
  set_all_registers(MAX7219_SHUTDOWN_REG, MAX7219_OFF);
  // drive 8 digits. datasheet table 8
  set_all_registers(MAX7219_SCANLIMIT_REG, 7);
  // no decode mode for all positions. datasheet table 4
  set_all_registers(MAX7219_DECODE_REG, B00000000);

  // clear matrix display
  clear_all_matrix();
}

void setup()  
{
  // init pin states
  pinMode(clock_pin, OUTPUT);
  pinMode(data_latch_pin, OUTPUT);    
  pinMode(data_input_pin, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  pinMode(MH, INPUT);
  pinMode(sensor_pin, INPUT);

  pinMode(SN1, INPUT);
  pinMode(SN2, INPUT);
  pinMode(SN3, INPUT);
  pinMode(SN4, INPUT);
    
  // init MAX2719 states
  init_all_max7219();

  Serial.begin(9600);
  BT.begin(9600);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

unsigned int starting_column_index = 0;

void loop()  
{
  int i, j;
  int target_column, target_word, word_num;
  char word_char;
  // turn off display first
  set_all_registers(MAX7219_SHUTDOWN_REG, MAX7219_OFF);
  
  // update all columns
  for (i = 0; i < NUM_OF_COLUMNS; i++)
  {
    digitalWrite(data_latch_pin, LOW);
    
    // update all matrixes
    for (j = NUM_OF_MATRIXES - 1; j >= 0; j--)
    {
      // jump to the correct column position for each matrix
      target_column = starting_column_index + NUM_OF_COLUMNS * j + i;
      target_word = target_column/(DISPLAY_COLUMN_LENGTH);
      //  make sure the target column is within the bitmap array
      target_column %= DISPLAY_COLUMN_LENGTH;
      word_char = dis[target_word%dis.length()];
      
      if((65<=word_char)&&(word_char<=90)){
        word_num = word_char - 65;
      }
      else if((97<=word_char)&&(word_char<=122)){
        word_num = word_char - 97;
      }
      else if((48<=word_char)&&(word_char<=57)){
        word_num = word_char - 19;
      }
      else if(word_char == ' '){
        word_num = 26;
      }
      else if(word_char == '!'){
        word_num = 28;
      }
      else if(word_char == 39){
        word_num = 39;
      }
      else{
        word_num = 27;
      }
      shiftOut(data_input_pin, clock_pin, MSBFIRST, MAX7219_COLUMN_REG(i));
      if(digitalRead(sensor_pin))
        shiftOut(data_input_pin, clock_pin, MSBFIRST, char_pattern[word_num][target_column]);
      else
        shiftOut(data_input_pin, clock_pin, MSBFIRST, blank_pattern[target_column]);
    }

    // latch the data pin to make the register data takes effect
    digitalWrite(data_latch_pin,HIGH);
  }
  
  // turn on display
  set_all_registers(MAX7219_SHUTDOWN_REG, MAX7219_ON);

  // step to the next column
  starting_column_index += 1;
  // go back to the first column of the string bitmap to be displayed
  if (starting_column_index >= DISPLAY_COLUMN_LENGTH*dis.length())
  {
    starting_column_index = 0;
  }
  if(BT.available() > 0){
    s = BT.readString();
    if(s.indexOf("<TITLE>")==0) {
      Serial.print(s);
      Serial.print('\n');
    }
    else if(s.indexOf("<NO>")==0) {
      Serial.print(s);
      Serial.print('\n');
    }
    else if(s.indexOf("<DEMO>")==0) {
      BT.print("Hey! your book is my favorite!");
      dis = "your book is my favorite!";
    }
    else if(s.indexOf("<push>")==0) {
      s.replace("<push>", "");
      if(s[0]=='L') {
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
        delay(1600);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
      }
      else if(s[0]=='R') {
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
        delay(1600);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
      }
      else {
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
      }
    }
    else if(s.indexOf("<dis>")==0) {
      s.replace("<dis>", "");
      dis = s;
      dis += " ";
    }
  }
  if(Serial.available() > 0){
    s = Serial.readString();
    if(s.indexOf("<dis>")==0) {
      s.replace("<dis>", "");
      dis = s;
      dis += " ";
    }
    else if(s.indexOf("<show>")==0) {
      s.replace("<show>", "");
      BT.print(s);
    }
    else if(s.indexOf("<showdis>")==0 || s.indexOf("<DATA>")==0) {
      s.replace("<showdis>", "");
      dis = s;
      dis += " ";
      BT.print(s);
    }
    else if(s.indexOf("<push>")==0) {
      s.replace("<push>", "");
      if(s[0]=='L') {
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
        delay(1600);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
      }
      else if(s[0]=='R') {
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
        delay(1600);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
      }
      else {
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
      }
    }
  }
  if(digitalRead(sensor_pin) and pressed){
    pressed = false;
  }
  if((not digitalRead(sensor_pin)) and (not pressed)){
    pressed = true;
    Serial.print("<book>");
    Serial.print('\n');
    s = "<SIGNAL>";
    for(int i = 0; i < 4; ++i){
      if(digitalRead(SN1+i)) s += "1";
      else s += "0";
    }
    Serial.print(s);
    Serial.print('\n');
  }
  delay(30);
}
