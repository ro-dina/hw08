import pygame as pg

# 初期化処理・グローバル変数
scale_factor = 3
chip_s = int(24*scale_factor) # マップチップ基本サイズ
map_s  = pg.Vector2(16,9)     # マップの横・縦の配置数 

# PlayerCharacterクラスの定義
class PlayerCharacter:

  # コンストラクタ
  def __init__(self,init_pos,img_path):
    self.pos  = pg.Vector2(init_pos)
    self.size = pg.Vector2(24,32)*scale_factor
    self.dir  = 2
    img_raw = pg.image.load(img_path)
    self.__img_arr = []
    for i in range(4):
      self.__img_arr.append([])
      for j in range(3):
        p = pg.Vector2(24*j,32*i)
        tmp = img_raw.subsurface(pg.Rect(p,(24,32)))
        tmp = pg.transform.scale(tmp, self.size)
        self.__img_arr[i].append(tmp)
      self.__img_arr[i].append(self.__img_arr[i][1])

    # 移動アニメーション関連
    self.is_moving = False  # 移動処理中は True になるフラグ
    self.__moving_vec = pg.Vector2(0,0) # 移動方向ベクトル
    self.__moving_acc = pg.Vector2(0,0) # 移動微量の累積

  def turn_to(self,dir):
    self.dir = dir

  def move_to(self,vec):
    self.is_moving = True
    self.__moving_vec = vec.copy()
    self.__moving_acc = pg.Vector2(0,0)
    self.update_move_process()
  
  def update_move_process(self):
    assert self.is_moving
    self.__moving_acc += self.__moving_vec * 10
    if self.__moving_acc.length() >= chip_s:
      self.pos += self.__moving_vec
      self.is_moving = False

  def get_dp(self):
    dp = self.pos*chip_s - pg.Vector2(0,12)*scale_factor
    if self.is_moving :  # キャラ状態が「移動中」なら
      dp += self.__moving_acc # 移動微量の累積値を加算
    return dp
  
  def get_img(self,frame):
    return self.__img_arr[self.dir][frame//6%4]

class Move:
    #コンストラクタ
    def __init__(self,img_path, block_type):
        self.image = pg.image.load(img_path)
        self.rect = self.image.get_rect()
        self.block_type = block_type #ブロックの種類を判別


    def draw(self, init_pos,screen):
        self.pos = pg.Vector2(init_pos)# 位置を追加
        screen.blit(self.image, self.pos) # 位置に基づいて画像を描画

    def fill(self, fill):
        fill_w, fill_h = fill.get_size()
        for y in range(0, fill_h, self.rect.height):
            for x in range(0, fill_w, self.rect.width):
                fill.blit(self.image, (x,y))



# ゲームループを含むメイン処理
def main():

  # 初期化処理
  pg.init() 
  pg.display.set_caption('ぼくのかんがえたさいきょうのげーむ II')
  map_s  = pg.Vector2(16,9)     # マップの横・縦の配置数 
  disp_w = int(chip_s*map_s.x)
  disp_h = int(chip_s*map_s.y)
  screen = pg.display.set_mode((disp_w,disp_h))
  clock  = pg.time.Clock()
  font   = pg.font.Font(None,15)
  frame  = 0
  exit_flag = False
  exit_code = '000'
  ground_option = 0
  framec = 0
  lock = 0
  font   = pg.font.Font('ipaexg.ttf',30)
  fontc   = pg.font.Font('ipaexg.ttf',100)

  game_map = [
    [5, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 0,],
    [3, 3, 3, 3, 3, 0, 3, 0, 0, 0, 3, 0, 3, 0, 3, 0,],
    [0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 3, 0, 3, 3,],
    [0, 3, 0, 3, 0, 0, 0, 0, 3, 3, 3, 0, 3, 0, 0, 3,],
    [0, 3, 3, 0, 3, 3, 3, 0, 0, 0, 3, 0, 0, 3, 0, 0,],
    [0, 0, 0, 0, 3, 1, 3, 0, 3, 0, 0, 3, 0, 3, 3, 0,],
    [0, 3, 3, 3, 3, 0, 3, 3, 0, 0, 3, 3, 0, 0, 0, 0,],
    [0, 0, 3, 0, 3, 0, 3, 0, 3, 0, 0, 0, 0, 3, 3, 0,],
    [3, 0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 3, 0, 0, 0, 0,]
]

  game_mapg = [
    [0, 0, 3, 3, 3, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0,],
    [3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 3, 0, 3,],
    [3, 0, 3, 3, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0,],
    [0, 0, 3, 3, 3, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 0,],
    [0, 3, 3, 0, 0, 0, 3, 0, 3, 3, 3, 0, 3, 3, 3, 0,],
    [0, 3, 0, 3, 3, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0,],
    [0, 3, 0, 0, 0, 0, 3, 3, 3, 0, 3, 3, 3, 0, 3, 0,],
    [0, 3, 3, 3, 3, 0, 0, 0, 3, 0, 0, 3, 0, 3, 3, 0,],
    [0, 0, 0, 3, 0, 0, 3, 3, 0, 0, 0, 3, 0, 0, 0, 0,]
]
  
  item = []

  # グリッド設定
  grid_c = '#bbbbbb'

  # 自キャラ移動関連
  cmd_move = -1 # 移動コマンドの管理変数
  m_vec = [
    pg.Vector2(0,-1),
    pg.Vector2(1,0),
    pg.Vector2(0,1),
    pg.Vector2(-1,0)
  ] # 移動コマンドに対応したXYの移動量

  #マップ生成
  ground_image = Move('./data/img/mainmap.png',0)
  ground_imageb = Move('./data/img/grassmap.png',0)


  # 自キャラの生成・初期化
  reimu = PlayerCharacter((2,3),'./data/img/reimu.png')
  
  #移動
  doorx = 5
  doory = 5
  firex = 0
  firey = 0
  exitx = 0
  exity = 0
  keyx = 9
  keyy = 3
  fire = Move('data/img/effect-fire.png',9)
  door = Move('data/img/door.png',1)
  block = Move('data/img/wall.png',3)
  key_ex = Move('data/img/key.png',6)
  exit = Move('data/img/exit.png',5)

  # ゲームループ
  while not exit_flag:

# システムイベントの検出
    for event in pg.event.get():
      if event.type == pg.QUIT: # ウィンドウ[X]の押下
        exit_flag = True
        exit_code = '001'

    # キー状態の取得
    key = pg.key.get_pressed()
    cmd_move = -1
    cmd_move = 0 if key[pg.K_w] else cmd_move
    cmd_move = 1 if key[pg.K_d] else cmd_move
    cmd_move = 2 if key[pg.K_s] else cmd_move
    cmd_move = 3 if key[pg.K_a] else cmd_move


    #screen.fill(pg.Color('black'))
    
    # 背景描画
    screen.fill(pg.Color('black'))

    if ground_option == 0:
        ground_image.fill(screen)
    
    elif ground_option == 1:
        ground_imageb.fill(screen)

    # グリッド
    for x in range(0, disp_w, chip_s): # 縦線
      pg.draw.line(screen,grid_c,(x,0),(x,disp_h))
    for y in range(0, disp_h, chip_s): # 横線
      pg.draw.line(screen,grid_c,(0,y),(disp_w,y))

    # 移動コマンドの処理
    if not reimu.is_moving:
        if cmd_move != -1:
            reimu.turn_to(cmd_move)
            af_pos = reimu.pos + m_vec[cmd_move]  # 仮移動した座標
            af_block_x = int(af_pos.x )
            af_block_y = int(af_pos.y )
            
            if ground_option == 0:
                # 範囲チェック
                if 0 <= af_block_x < len(game_map[0]) and 0 <= af_block_y < len(game_map):
                    af_block_type = game_map[af_block_y][af_block_x]
                    if af_block_type != 3:
                        if (0 <= af_pos.x <= map_s.x-1) and (0 <= af_pos.y <= map_s.y-1):
                            reimu.move_to(m_vec[cmd_move])  # 画面範囲内なら移動指示
            
            if ground_option == 1:
                if 0 <= af_block_x < len(game_map[0]) and 0 <= af_block_y < len(game_map):
                    af_block_type = game_mapg[af_block_y][af_block_x]
                    if af_block_type != 3:
                        if (0 <= af_pos.x <= map_s.x-1) and (0 <= af_pos.y <= map_s.y-1):
                            reimu.move_to(m_vec[cmd_move])  # 画面範囲内なら移動指示
            


    # キャラが移動中ならば、移動アニメ処理の更新
    if reimu.is_moving:
        reimu.update_move_process()

    # 自キャラの描画
    screen.blit(reimu.get_img(frame),reimu.get_dp())

    # エフェクトの描画
    door.draw((doorx*72, doory*72),screen)

    if ground_option == 0:
        fire.draw((firex*72,firey*72),screen)
        exit.draw((exitx*72,exity*72),screen)

    if ground_option == 1 and 6 not in item:
        key_ex.draw((keyx*72,keyy*72),screen)

    if 6 in item:
        game_map[2][5] = 3

    #障害物の配置
    if ground_option == 0:

        for y in range(len(game_map)):
            for x in range(len(game_map[0])):
                if game_map[y][x] == 3:
                    block.draw((x*72, y*72), screen)
    
    elif ground_option == 1:

        for y in range(len(game_mapg)):
            for x in range(len(game_mapg[0])):
                if game_mapg[y][x] == 3:
                    block.draw((x*72, y*72), screen)


    # フレームカウンタの描画
    if framec == 0:
        frame += 1
        frm_str = f'{frame:05}'
        screen.blit(font.render(frm_str,True,'BLACK'),(10,10))
        screen.blit(font.render(f'{reimu.pos}',True,'BLACK'),(10,20))

    elif framec == 1 :
        gool_img = 'クリア'
        frm_str = f'{gool_img}'
        screen.blit(fontc.render(frm_str,True,'yellow'),(6*72,3*72))
        frm_str = f'{frame}'
        screen.blit(font.render(frm_str,True,'black'),(7.5*72,4.5*72))



    #鍵ドアの処理
    if reimu.pos.x == exitx and reimu.pos.y == exity and 6 in item:
       lock += 1
    
    if reimu.pos.x == exitx and reimu.pos.y == exity and 6 not in item and af_block_type == 5:
        keytxt = '鍵が必要'
        frm_str = f'{keytxt}'
        screen.blit(fontc.render(frm_str,True,'blue'),(6*72,3*72))
    
    else:
        keytxt = ''

    
    # 画面の更新と同期
    pg.display.update()
    clock.tick(30)
 
    #ドアとの座標の比較処理
    if reimu.pos.x == doorx and reimu.pos.y == doory and ground_option == 0:
      ground_option += 1
      doory += 3
      reimu.pos.y+=2
    
    elif reimu.pos.x == doorx and reimu.pos.y == doory and ground_option == 1:
       ground_option -= 1
       doory -= 3
       reimu.pos.y-=2
    
    else:
       keytxt = ''
    
    #鍵の処理
    if reimu.pos.x == keyx and reimu.pos.y == keyy:
        item.append(6)


    #ゴール処理
    if reimu.pos.x == exitx and reimu.pos.y == exity and framec == 0 and lock == 1:
        framec += 1



  # ゲームループ [ここまで]
  pg.quit()
  return exit_code

if __name__ == "__main__":
  code = main()
  print(f'プログラムを「コード{code}」で終了しました。')