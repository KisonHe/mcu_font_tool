// This is a Processing sketch, see https://processing.org/ to download the IDE

// Select the font, size and character ranges in the user configuration section
// of this sketch, which starts at line 120. Instructions start at line 50.


/*
Software License Agreement (FreeBSD License)
 
 Copyright (c) 2018 Bodmer (https://github.com/Bodmer)
 
 All rights reserved.
 
 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions are met:
 
 1. Redistributions of source code must retain the above copyright notice, this
 list of conditions and the following disclaimer.
 2. Redistributions in binary form must reproduce the above copyright notice,
 this list of conditions and the following disclaimer in the documentation
 and/or other materials provided with the distribution.
 
 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
 ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
 WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
 ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
 ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 
 The views and conclusions contained in the software and documentation are those
 of the authors and should not be interpreted as representing official policies,
 either expressed or implied, of the FreeBSD Project.
 */

////////////////////////////////////////////////////////////////////////////////////////////////

// This is a processing sketch to create font files for the TFT_eSPI library:

// https://github.com/Bodmer/TFT_eSPI

// Coded by Bodmer January 2018, updated 10/2/19
// Version 0.8

// >>>>>>>>>>>>>>>>>>>>             INSTRUCTIONS             <<<<<<<<<<<<<<<<<<<<

// See comments below in code for specifying the font parameters (point size,
// unicode blocks to include etc). Ranges of characters (glyphs) and specific
// individual glyphs can be included in the created "*.vlw" font file.

// Created fonts are saved in the sketches "FontFiles" folder. Press Ctrl+K to
// see that folder location.

// 16 bit Unicode point codes in the range 0x0000 - 0xFFFF are supported.
// Codes 0-31 are control codes such as "tab" and "carraige return" etc.
// and 32 is a "space", these should NOT be included.

// The sketch will convert True Type (a .ttf or .otf file) file stored in the
// sketches "Data" folder as well as your computers' system fonts.

// To maximise rendering performance and the memory consumed only include the characters
// you will use. Characters at the start of the file will render faster than those at
// the end due to the buffering and file seeking overhead.

// The inclusion of "non-existant" characters in a font may give unpredicatable results
// when rendering with the TFT_eSPI library. The Processing sketch window that pops up
// to show the font characters will print "boxes" (also known as Tofu!) for non existant
// characters.

// Once created the files must be loaded into the ESP32 or ESP8266 SPIFFS memory
// using the Arduino IDE plugin detailed here:
// https://github.com/esp8266/arduino-esp8266fs-plugin
// https://github.com/me-no-dev/arduino-esp32fs-plugin

// When the sketch is run it will generate a file called "System_Font_List.txt" in the
// sketch "FontFiles" folder, press Ctrl+K to see it. Open the file in a text editor to
// view it. This list provides the font reference number needed below to locate that
// font on your system.

// The sketch also lists all the available system fonts to the console, you can increase
// the console line count (in preferences.txt) to stop some fonts scrolling out of view.
// See link in File>Preferences to locate "preferences.txt" file. You must close
// Processing then edit the file lines. If Processing is not closed first then the
// edits will be overwritten by defaults! Edit "preferences.txt" as follows for
// 3000 lines, then save, then run Processing again:

//     console.length=3000;             // Line 4 in file
//     console.scrollback.lines=3000;   // Line 7 in file


// Useful links:
/*

 https://en.wikipedia.org/wiki/Unicode_font
 
 https://www.gnu.org/software/freefont/
 https://www.gnu.org/software/freefont/sources/
 https://www.gnu.org/software/freefont/ranges/
 http://savannah.gnu.org/projects/freefont/
 
 http://www.google.com/get/noto/
 
 https://github.com/Bodmer/TFT_eSPI
 https://github.com/esp8266/arduino-esp8266fs-plugin
 https://github.com/me-no-dev/arduino-esp32fs-plugin
 
   >>>>>>>>>>>>>>>>>>>>         END OF INSTRUCTIONS         <<<<<<<<<<<<<<<<<<<< */


import java.awt.Desktop; // Required to allow sketch to open file windows


////////////////////////////////////////////////////////////////////////////////////////////////

//                       >>>>>>>>>> USER CONFIGURED PARAMETERS START HERE <<<<<<<<<<

// Use font number or name, -1 for fontNumber means use fontName below, a value >=0 means use system font number from list.
// When the sketch is run it will generate a file called "systemFontList.txt" in the sketch folder, press Ctrl+K to see it.
// Open the "systemFontList.txt" in a text editor to view the font files and reference numbers for your system.
// << Use [Number] in brackets from the fonts listed.


// Define the font size in points for the TFT_eSPI font file
// Font size to use in the Processing sketch display window that pops up (can be different to above)
String goodFontName = "";
//>>fontNumber Start
int fontNumber = 732;
String fontName = "Final-Frontier";
String fontType = ".ttf";
int fontSize = 50;
int displayFontSize = 50;//>>fontNumber End
//String fontType = ".otf";



// OR use font name for ttf files placed in the "Data" folder or the font number seen in IDE Console for system fonts
//                                                  the font numbers are listed when the sketch is run.
//                |         1         2     |       Maximum filename size for SPIFFS is 31 including leading /
//                 1234567890123456789012345        and added point size and .vlw extension, so max is 25
// Manually crop the filename length later after creation if needed
// Note: SPIFFS does NOT accept underscore in a filename!


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Next we specify which unicode blocks from the the Basic Multilingual Plane (BMP) are included in the final font file. //
// Note: The ttf/otf font file MAY NOT contain all possible Unicode characters, refer to the fonts online documentation. //
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


// The list below has been created from the table here: https://en.wikipedia.org/wiki/Unicode_block
// Remove // at start of lines below to include that unicode block, different code ranges can also be specified by
// editting the start and end-of-range values. Multiple lines from the list below can be included, limited only by
// the final font file size!

// Block range,   //Block name, Code points, Assigned characters, Scripts
// First, last,   //Range is inclusive of first and last codes
// 0x0021, 0x007E, //Basic Latin, 128, 128, Latin (52 characters), Common (76 characters)
//>>unicodeBlocks Start
static final int[] unicodeBlocks = {

};
//>>unicodeBlocks End

// Here we specify particular individual Unicodes to be included (appended at end of selected range)
//>>specificUnicodes Start
static final int[] specificUnicodes = {
69, 110, 103, 108, 105, 115, 104, 31616, 20307, 20013, 25991, 26085, 26412, 35486, 20320, 22909, 120, 99, 101, 112, 116, 67, 33, 12371, 12435, 12395, 12385, 12399, 72, 111, 84, 97, 83, 114
};
//>>specificUnicodes End

//                       >>>>>>>>>> USER CONFIGURED PARAMETERS END HERE <<<<<<<<<<

////////////////////////////////////////////////////////////////////////////////////////////////

// Variable to hold the inclusive Unicode range (16 bit values only for this sketch)
int firstUnicode = 0;
int lastUnicode  = 0;

PFont myFont;

PrintWriter logOutput;

void setup() {
  logOutput = createWriter("FontFiles/System_Font_List.txt"); 

  size(1000, 800);

  // Print the available fonts to the console as a list:
  String[] fontList = PFont.list();
  // printArray(fontList);

  // Save font list to file
  for (int x = 0; x < fontList.length; x++)
  {
    logOutput.print("[" + x + "] ");
    logOutput.println(fontList[x]);
  }
  logOutput.flush(); // Writes the remaining data to the file
  logOutput.close(); // Finishes the file

  // Set the fontName from the array number or the defined fontName
  if (fontNumber >= 0)
  {
    fontName = fontList[fontNumber];
    fontType = "";
  }

  char[]   charset;
  int  index = 0, count = 0;

  int blockCount = unicodeBlocks.length;

  for (int i = 0; i < blockCount; i+=2) {
    firstUnicode = unicodeBlocks[i];
    lastUnicode  = unicodeBlocks[i+1];
    if (lastUnicode < firstUnicode) {
      delay(100);
      System.err.println("ERROR: Bad Unicode range secified, last < first!");
      System.err.print("first in range = 0x" + hex(firstUnicode, 4));
      System.err.println(", last in range  = 0x" + hex(lastUnicode, 4));
      while (true);
    }
    // calculate the number of characters
    count += (lastUnicode - firstUnicode + 1);
  }

  count += specificUnicodes.length;

  println();
  println("=====================");
  println("Creating font file...");
  println("Unicode blocks included     = " + (blockCount/2));
  println("Specific unicodes included  = " + specificUnicodes.length);
  println("Total number of characters  = " + count);

  if (count == 0) {
    delay(100);
    System.err.println("ERROR: No Unicode range or specific codes have been defined!");
    while (true);
  }

  // allocate memory
  charset = new char[count];

  for (int i = 0; i < blockCount; i+=2) {
    firstUnicode = unicodeBlocks[i];
    lastUnicode  =  unicodeBlocks[i+1];

    // loading the range specified
    for (int code = firstUnicode; code <= lastUnicode; code++) {
      charset[index] = Character.toChars(code)[0];
      index++;
    }
  }

  // loading the specific point codes
  for (int i = 0; i < specificUnicodes.length; i++) {
    charset[index] = Character.toChars(specificUnicodes[i])[0];
    index++;
  }

  // Make font smooth (anti-aliased)
  boolean smooth = true;

  // Create the font in memory
  myFont = createFont(fontName+fontType, displayFontSize, smooth, charset);

  // Print characters to the sketch window
  fill(0, 0, 0);
  textFont(myFont);

  // Set the left and top margin
  int margin = displayFontSize;
  translate(margin/2, margin);

  int gapx = displayFontSize*10/8;
  int gapy = displayFontSize*10/8;
  index = 0;
  fill(0);

  textSize(displayFontSize);

  for (int y = 0; y < height-gapy; y += gapy) {
    int x = 0;
    while (x < width) {

      int unicode = charset[index];
      float cwidth = textWidth((char)unicode) + 2;
      if ( (x + cwidth) > (width - gapx) ) break;

      // Draw the glyph to the screen
      text(new String(Character.toChars(unicode)), x, y);

      // Move cursor
      x += cwidth;
      // Increment the counter
      index++;
      if (index >= count) break;
    }
    if (index >= count) break;
  }


  // creating font to save as a file
  PFont    font;

  font = createFont(fontName+fontType, fontSize, smooth, charset);

  println("Created font " + fontName + str(fontSize) + ".vlw");

  // creating file
  try {
    print("Saving to sketch FontFiles folder... ");
    goodFontName = fontName.replace(' ','-');
    // a-123-b
    while (goodFontName.indexOf("-") != -1){
      String first = "";
      String end = "";
      // SPIFFS dont like '-'
      first = goodFontName.substring(0,goodFontName.indexOf("-")); //"-" wont be first and last char
      end = goodFontName.substring(goodFontName.indexOf("-") + 1,goodFontName.length());
      goodFontName = first + end;
    }
    if (goodFontName.length() > 20){
      // SPIFFS dont like filename too long
      goodFontName = goodFontName.substring(goodFontName.length() - 20, goodFontName.length());
    }
    OutputStream output = createOutput("FontFiles/" + goodFontName + str(fontSize) + ".vlw");
    font.save(output);
    output.close();

    println("OK!");

    delay(100);

    // Open up the FontFiles folder to access the saved file
    String path = sketchPath();
    // Desktop.getDesktop().open(new File(path+"/FontFiles"));

    // System.err.println("All done! Note: Rectangles are displayed for non-existant characters.");
    println("All done! Note: Rectangles are displayed for non-existant characters.");
  }
  catch(Exception e) {
    print(e);
    println("Something is wrong");
  }
}
