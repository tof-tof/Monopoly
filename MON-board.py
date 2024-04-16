def get_location(general_gameState):
   bb_coor_list=[(480, 530), (360, 530), (240, 530), (120, 530), (0, 530), (0, 410), (0, 290), (0, 170), (0, 50), (120, 50),(240, 50), (360, 50), (480, 50), (480, 170), (480, 290), (480, 410)]
   hat_coor_list=[(550, 530), (430, 530), (310, 530), (190, 530), (70, 530), (70, 410), (70, 290), (70, 170), (70, 50), (190, 50),(310, 50), (430, 50), (550, 50), (550, 170), (550, 290), (550, 410)]
   location_list=[]
   for name in general_gameState["player_info"]:
       location=general_gameState["player_info"][name]["current_location"]
       location_list.append(location)
   bb_coor=bb_coor_list[location_list[0]]
   hat_coor=hat_coor_list[location_list[1]]
   return [bb_coor,hat_coor]

def drawBoard(width, height, gameState):
    html = '<!DOCTYPE html><html><head>'
    # TODO Add CSS
    html += '</head>'
    html += '<body>'
    html += '<img hidden id="battleship" src="battleship.png" alt="Battleship" width="70" height="70">'
    html += '<img hidden id="hat" src="hat.png" alt="hat" width="70" height="70">'
    html += '<img hidden id="chance" src="monoImages\\chance2.jpg" alt="chance" width="70" height="70">'
    html += '<img hidden id="liberty" src="monoImages\\liberty1.jpg" alt="chance" width="70" height="70">'
    html += '<img hidden id="bridge" src="monoImages\\bridge2.jpg" alt="chance" width="70" height="70">'
    html += '<img hidden id="Alcatraz" src="monoImages\\Alcatraz2.jpg" alt="chance" width="70" height="70">'
    html += '<img hidden id="EffielTower" src="monoImages\\"EffielTower2".jpg" alt="chance" width="70" height="70">'
    html += '<img hidden id="Christ" src="monoImages\\Christ1.jpg" alt="chance" width="70" height="70">'
    html += '<img hidden id="OperaHouse" src="monoImages\\OperaHouse1.jpg" alt="chance" width="70" height="70">'
    html += '<canvas id="myCanvas" width= "%d" height="%d" style="border:5px solid #162235;"> ' % (width,height)
    html += 'Your browser does not support the HTML5 canvas tag.</canvas>'
# 900 -200 width-tileWidth
    html += '''<script>
                var c = document.getElementById("myCanvas");
                var ctx = c.getContext("2d");'''
    #left line, right line, top line, bottom line
    html +='''  ctx.moveTo(120,0);
                ctx.lineTo(120,%d);
                ctx.moveTo(480,0);
                ctx.lineTo(480,%d);
                ctx.moveTo(0,120);
                ctx.lineTo(%d,120);
                ctx.moveTo(0,480);
                ctx.lineTo(%d,480);'''%(height,height,width,width)
    #inter = intermediate
    #top inter line, bottom inter line, left inter line, right inter line
    html+='''   ctx.moveTo(0, 240);
                ctx.lineTo(120,240);
                ctx.moveTo(480,240);
                ctx.lineTo(%d, 240);
                
                ctx.moveTo(0,360);
                ctx.lineTo(120,360);
                ctx.moveTo(480,360);
                ctx.lineTo(%d,360);
                
                ctx.moveTo(240,0);
                ctx.lineTo(240,120);
                ctx.moveTo(240,480);
                ctx.lineTo(240,%d);
                
                ctx.moveTo(360,0);
                ctx.lineTo(360,120);
                ctx.moveTo(360,480);
                ctx.lineTo(360,%d);
                
                ctx.stroke();
                ''' %(height, height,width,width)

    html += '''
                var go=c.getContext("2d");
                //go.rotate(-Math.PI*2/(6));
                go.font="35px Verdana";
                // Create gradient
                var gradient=ctx.createLinearGradient(0,0,c.width,0);
                gradient.addColorStop("0","magenta");
                gradient.addColorStop("0.5","blue");
                gradient.addColorStop("1.0","red");
                // Fill with gradient
                go.fillStyle=gradient;
                
                go.fillText("GO!",510,540);'''

    html += '''
                  var col=c.getContext("2d");

                  col.font="19px Verdana";
                  // Create gradient
                  var gradient=ctx.createLinearGradient(0,0,c.width,0);
                  gradient.addColorStop("0","magenta");
                  gradient.addColorStop("0.5","blue");
                  gradient.addColorStop("1.0","red");
                  // Fill with gradient
                  col.fillStyle=gradient;
                  col.fillText("collect %d",487,570);''' %(gameState["go_money"])


    html += '''
                var jail=c.getContext("2d");
                jail.font="35px Verdana";
                // Create gradient
                var gradient2=ctx.createLinearGradient(0,0,c.width,0);
                gradient2.addColorStop("0","magenta");
                gradient2.addColorStop("0.5","blue");
                gradient2.addColorStop("1.0","red");
                // Fill with gradient
                jail.fillStyle=gradient2;
                jail.fillText("JAIL",25,75);
                '''

    [(bbx, bby), (hatx, haty)] = get_location(gameState)
    html += '''window.onload = function() {
              var b = c.getContext("2d");
              var img = document.getElementById("battleship");
              b.drawImage(img,%d,%d,70,70);
              var img1 = document.getElementById("hat");
             // b.rotate(20 * Math.PI / 180);
              var img2 = document.getElementById("chance");
              b.drawImage(img1,%d,%d,50,50);
              b.drawImage(img2,0,480,120,120);
              b.drawImage(img2,480,0,120,120);
              var img3 = document.getElementById("liberty");
              b.drawImage(img3,360,480,120,120);
              var img4 = document.getElementById("bridge");
              b.drawImage(img4,240,480,120,120);
              var img5 = document.getElementById("Christ");
              b.drawImage(img5,0,120,120,120);
              var img7 = document.getElementById("Alcatraz");
              b.drawImage(img7,120,0,120,120);
              var img8 = document.getElementById("OperaHouse");
              b.drawImage(img8,240,0,120,120);
              
              var img6 = document.getElementById("EffielTower");
              b.drawImage(img6,0,240,120,120);
              }
              </script><br>''' % (bbx, bby, hatx, haty)

    html += '<h2>Move Number</h2>' + str(gameState["move_number"])
    html += '<h2>Mover</h2>' + str(gameState["Mover"])




    html += '</body></html>'

    return html

if __name__=="__main__":
    gs = {
                "board": [
                    [
                        0,
                        1,
                        2,
                        3
                    ],
                    [
                        4,
                        5,
                        6,
                        7
                    ],
                    [
                        8,
                        9,
                        10,
                        11
                    ],
                    [
                        12,
                        13,
                        14,
                        15
                    ]
                ],
                "board_size": 4,
                "place_database": {
                    0: {
                        "name": "start",
                        "images": [
                            "Links"
                        ],
                        "owner": -2
                    },
                    1: {
                        "name": "The Statue of Liberty",
                        "buyPrice": 10,
                        "Rent": 1,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    2: {
                        "name": "Golden Gate Bridge",
                        "buyPrice": 20,
                        "Rent": 2,
                        "owner": 0,
                        "images": [
                            "Links"
                        ]
                    },
                    3: {
                        "name": "Effiel Tower",
                        "buyPrice": 30,
                        "Rent": 3,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    4: {
                        "name": "Community Chest",
                        "owner": -2,
                        "images": [
                            "Links"
                        ]
                    },
                    5: {
                        "name": "St. Basil\'s Cathedral",
                        "buyPrice": 40,
                        "Rent": 4,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    6: {
                        "name": " Burj Khalifa",
                        "buyPrice": 50,
                        "Rent": 5,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    7: {
                        "name": "Christ the Redeemer",
                        "buyPrice": 60,
                        "Rent": 6,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    8: {
                        "name": "jail",
                        "owner": -2,
                        "images": [
                            "Links"
                        ]
                    },
                    9: {
                        "name": " Sydney Opera House",
                        "buyPrice": 70,
                        "Rent": 7,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    10: {
                        "name": "The Pyramids of Giza",
                        "buyPrice": 80,
                        "Rent": 8,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    11: {
                        "name": " Alcatraz",
                        "buyPrice": 90,
                        "Rent": 9,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    12: {
                        "name": "chance",
                        "owner": -2,
                        "images": [
                            "Links"
                        ]
                    },
                    13: {
                        "name": "The Great Wall of China",
                        "buyPrice": 100,
                        "Rent": 10,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    14: {
                        "name": "Taj Mahal",
                        "buyPrice": 110,
                        "Rent": 11,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    },
                    15: {
                        "name": "Tower of Pisa",
                        "buyPrice": 120,
                        "Rent": 12,
                        "owner": -1,
                        "images": [
                            "Links"
                        ]
                    }
                },
                "player_info": {
                    "AAA": {
                        "money": 2000,
                        "in_jail": False,
                        "on_CH": False,
                        "current_location": 15,
                        "hasGOJ": False,
                        "in_game": True
                    },
                    "BBB": {
                        "money": 2000,
                        "in_jail": False,
                        "on_CH": False,
                        "current_location": 8,
                        "hasGOJ": False,
                        "in_game": True
                    }
                },
                "Mover": 0,
                "response_deadline": 1552489463683000,
                "game_deadline": 1552489562683000,
                "move_number": 0,
                "bribe": 500,
                "go_money": 1000,
                "move_limit": 100
            }
    f = open("MON-Board.html", "w")
    HTML = drawBoard(600,600,gs)
    f.write(HTML)