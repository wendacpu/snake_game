import pygame
import random

# 初始化pygame
pygame.init()

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 55, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
gray = (169, 169, 169)  # 障碍物颜色
yellow = (255, 255, 0)  # 按钮颜色

# 设置显示窗口
display_width = 1200
display_height = 800
dis = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('贪吃蛇游戏')

# 设置游戏时钟
clock = pygame.time.Clock()

# 蛇的大小和速度
snake_block = 40  # 增大蛇的大小，使其更容易看见
snake_speed = 8  # 降低速度，使游戏更容易控制

# 设置字体
font_name = pygame.font.match_font('Pristina')
font_title = pygame.font.Font("Songti.ttc", 36)
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
title_font = pygame.font.SysFont("bahnschrift", 70)
button_font = pygame.font.SysFont("bahnschrift", 40)

# 加载音效文件
try:
    eat_sound = pygame.mixer.Sound(r'music/eat.mp3')  # 吃食物音效
    crash_sound = pygame.mixer.Sound(r'music/crash.mp3')  # 碰撞音效
    start_sound = pygame.mixer.Sound(r'music/start.wav')  # 开始游戏音效
    game_over_sound = pygame.mixer.Sound(r'music/game_over.wav')  # 结束游戏音效
    button_click_sound = pygame.mixer.Sound(r'music/click.wav')  # 按钮点击音效
    background_music = r'music/bg.wav'  # 背景音乐
except:
    print("警告: 未能加载所有音效文件，游戏将继续但没有音效")
    # 创建空音效对象以避免报错
    eat_sound = pygame.mixer.Sound(buffer=bytearray(0))
    crash_sound = pygame.mixer.Sound(buffer=bytearray(0))
    start_sound = pygame.mixer.Sound(buffer=bytearray(0))
    game_over_sound = pygame.mixer.Sound(buffer=bytearray(0))
    button_click_sound = pygame.mixer.Sound(buffer=bytearray(0))
    background_music = None

#载入背景图和半透明覆盖层
background1 = pygame.image.load('pictures/background/bgd2/bg2_ori._alpha.png').convert_alpha()
background2 = pygame.image.load('pictures/background/bgd5/bgd5_alpha.png').convert_alpha()
background3 = pygame.image.load('pictures/background/bgd3/bgd3_alpha.png').convert_alpha()
#background = pygame.image.load('pictures/background/bgd1/backgrs_alpha.jpg').convert_alpha()
background1 = pygame.transform.scale(background1, (display_width, display_height))
background2 = pygame.transform.scale(background2, (display_width, display_height))
background3 = pygame.transform.scale(background3, (display_width, display_height))
#overlay = pygame.Surface((display_width, display_height), pygame.SRCALPHA)
#overlay.fill((255, 255, 255, 200))

# 蛇类
# 蛇类
class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_change = snake_block
        self.y_change = 0
        self.body = []
        self.length = 3  # 初始长度设为3，更容易看到

        # 初始化蛇的身体
        self.head = []
        self.head.append(x)
        self.head.append(y)
        self.body.append(self.head.copy())

        # 添加无敌时间
        self.invincible_start_time = pygame.time.get_ticks()
        self.invincible_duration = 2000

        #加载图片
        self.head_img = pygame.image.load('pictures/Snake_head/Snake_head6.png').convert_alpha()
        self.body_img = pygame.image.load('pictures/Snake_body/Snake_body1.png').convert_alpha()
        self.head_img = pygame.transform.scale(self.head_img, (snake_block, snake_block))
        self.body_img = pygame.transform.scale(self.body_img, (snake_block, snake_block))

        # 存储不同方向的蛇头
        self.head_directions = {
            "RIGHT": self.head_img,
            "LEFT": pygame.transform.rotate(self.head_img, 180),
            "UP": pygame.transform.rotate(self.head_img, 90),
            "DOWN": pygame.transform.rotate(self.head_img, 270)
        }


    def move(self):
        # 更新蛇的位置
        self.x += self.x_change
        self.y += self.y_change

        # 边界穿越逻辑
        if self.x >= display_width:
            self.x = 0
        elif self.x < 0:
            self.x = display_width - snake_block
        if self.y >= display_height:
            self.y = 0
        elif self.y < 0:
            self.y = display_height - snake_block

        # 更新蛇的头部
        self.head = []
        self.head.append(self.x)
        self.head.append(self.y)
        self.body.append(self.head.copy())

        # 如果蛇的长度超过了应有的长度，删除多余的部分
        if len(self.body) > self.length:
            del self.body[0]

    def change_direction(self, direction):
        if direction == "LEFT" and self.x_change != snake_block:  # 防止直接反向移动
            self.x_change = -snake_block
            self.y_change = 0
        elif direction == "RIGHT" and self.x_change != -snake_block:
            self.x_change = snake_block
            self.y_change = 0
        elif direction == "UP" and self.y_change != snake_block:
            self.y_change = -snake_block
            self.x_change = 0
        elif direction == "DOWN" and self.y_change != -snake_block:
            self.y_change = snake_block
            self.x_change = 0

    def current_direction(self):  #新增一个方法来判断蛇头方向
        if self.x_change > 0: return "RIGHT"
        if self.x_change < 0: return "LEFT"
        if self.y_change < 0: return "UP"
        if self.y_change > 0: return "DOWN"

    def draw(self):
        # 绘制蛇头（不同颜色，自动匹配方向）
        if len(self.body) > 0:
            head = self.body[-1]

            direction = self.current_direction()
            dis.blit(self.head_directions[direction], (self.head[0], self.head[1]))
            #pygame.draw.rect(dis, blue, [head[0], head[1], snake_block, snake_block])

        # 绘制蛇身
        for segment in self.body[:-1]:
            dis.blit(self.body_img, (segment[0], segment[1]))
            #pygame.draw.rect(dis, gray, [segment[0], segment[1], snake_block, snake_block])

    def check_collision_with_self(self):
        # 检查是否撞到自己
        for segment in self.body[:-1]:
            if segment == self.head:
                return True
        return False

    # def check_collision_with_boundaries(self):
    #     # 检查是否撞到边界
    #     if self.x >= display_width or self.x < 0 or self.y >= display_height or self.y < 0:
    #         return True
    #     return False

    def check_collision_with_obstacle(self, obstacle):
        # 检查是否撞到障碍物
        #return self.head == obstacle.position
        head_rect = pygame.Rect(self.head[0], self.head[1],snake_block, snake_block)
        obstacle_rect = obstacle.get_rect()
        # 无敌时间判断
        if pygame.time.get_ticks() - self.invincible_start_time < self.invincible_duration:
            return False
        return head_rect.colliderect(obstacle_rect)


    def check_collision_with_food(self, food):
        # 检查是否吃到食物
        return self.x == food.x and self.y == food.y

    def grow(self):
        # 增加蛇的长度
        self.length += 1


# 食物类
class Food:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.position = [self.x, self.y]
        self.is_big_reward = False  # 是否是大奖励
        self.big_reward_multiplier = 3  # 大奖励的分数倍数

        #加载Food以及分数奖励图片
        self.normal_image = pygame.image.load('pictures/food/food.png').convert_alpha()
        self.big_image = pygame.image.load('pictures/food/big_food.jpg').convert_alpha()
        self.normal_image = pygame.transform.scale(self.normal_image, (snake_block, snake_block))
        self.big_image = pygame.transform.scale(self.big_image, (snake_block*1.5, snake_block*1.5))

        self.respawn()

    def respawn(self, obstacles=None, snake_body=None,score=0):
        # 检查是否应该生成大奖励(每10分一个阶段)
        self.is_big_reward = score > 0 and score % 10 == 0

        # 随机生成食物位置
        self.x = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
        self.y = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
        self.position = [self.x, self.y]

        # 确保食物不在障碍物上和蛇身上
        if obstacles and snake_body:
            while self.position in [obstacle.position for obstacle in obstacles] or self.position in snake_body:
                self.x = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
                self.y = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
                self.position = [self.x, self.y]

        # 检查是否与障碍物冲突
        valid = True
        if obstacles:
            for obstacle in obstacles:
                obstacle_rect = obstacle.get_rect()
                food_rect = pygame.Rect(self.x, self.y, snake_block, snake_block)
                if food_rect.colliderect(obstacle_rect):
                    valid = False
                    break
                if valid and (snake_body is None or self.position not in snake_body):
                    break

    def draw(self):
        # 根据食物类型绘制不同图像
        if self.is_big_reward:
            # 大奖励食物会闪烁以吸引注意
            if pygame.time.get_ticks() % 500 < 250:  # 每500ms闪烁一次
                dis.blit(self.big_image, (self.x - snake_block * 0.25, self.y - snake_block * 0.25))  # 居中显示
        else:
            dis.blit(self.normal_image, (self.x, self.y))
        # pygame.draw.rect(dis, red, [self.x, self.y, snake_block, snake_block])


# 障碍物类
class Obstacle:

    # 类变量，存储所有可能的障碍物图片
    obstacle_images = [
        'pictures/obstacles/obstacle1.png',
        'pictures/obstacles/obstacle2.png',
        'pictures/obstacles/obstacle3.png',
        'pictures/obstacles/obstacle4.png',
        'pictures/obstacles/obstacle5.png',
    ]

    # 记录已使用的图片索引，确保不重复
    used_images = []

    def __init__(self, x=None, y=None):
        if x is None or y is None:
            self.x = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
            self.y = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
        else:
            self.x = x
            self.y = y
        self.position = [self.x, self.y]


        # 随机选择一个未使用过的图片
        if not Obstacle.used_images:
            # 第一次使用时，重置并打乱顺序
            Obstacle.used_images = list(range(len(Obstacle.obstacle_images)))
            random.shuffle(Obstacle.used_images)

        img_index = Obstacle.used_images.pop()
        img_path = Obstacle.obstacle_images[img_index]

        # 加载障碍物图片
        self.img = pygame.image.load(img_path).convert_alpha()
        self.img = pygame.transform.scale(self.img, (snake_block *2, snake_block*2))

    def get_rect(self):
        #获取其矩形与snake_head的矩形做碰撞检测
        return pygame.Rect(self.x, self.y, snake_block*2, snake_block*2)

    def draw(self):
        # 绘制障碍物
        dis.blit(self.img, (self.x, self.y))
        #pygame.draw.rect(dis, black, [self.x, self.y, snake_block, snake_block])

    def respawn(self, snake_head, snake_direction, obstacles, snake_body, food_position):
        """改进后的生成逻辑"""
        start_time = pygame.time.get_ticks()  # 防止无限循环
        max_attempts = 50  # 最大尝试次数

        for _ in range(max_attempts):
            # 生成候选位置
            self.x = round(random.randrange(0, display_width - snake_block * 2) / snake_block) * snake_block
            self.y = round(random.randrange(0, display_height - snake_block * 2) / snake_block) * snake_block
            self.position = [self.x, self.y]

            # ---- 安全检测 ----
            safe = True

            # 规则1：远离其他障碍物（至少2个蛇身距离）
            for other in obstacles:
                if self != other:
                    dx = abs(self.x - other.x)
                    dy = abs(self.y - other.y)
                    if dx < snake_block * 2 and dy < snake_block * 2:
                        safe = False
                        break

            # 规则2：不在蛇前进方向的前方区域（预测未来3步）
            if snake_direction == "RIGHT":
                danger_zone = pygame.Rect(snake_head[0] + snake_block, snake_head[1] - snake_block * 3, snake_block * 5,
                                          snake_block * 7)
            elif snake_direction == "LEFT":
                danger_zone = pygame.Rect(snake_head[0] - snake_block * 5, snake_head[1] - snake_block * 3,
                                          snake_block * 5, snake_block * 7)
            elif snake_direction == "UP":
                danger_zone = pygame.Rect(snake_head[0] - snake_block * 3, snake_head[1] - snake_block * 5,
                                          snake_block * 7, snake_block * 5)
            else:  # DOWN
                danger_zone = pygame.Rect(snake_head[0] - snake_block * 3, snake_head[1] + snake_block, snake_block * 7,
                                          snake_block * 5)

            if danger_zone.collidepoint((self.x, self.y)):
                safe = False

            # 规则3：不与蛇身/食物重叠
            if any(segment == self.position for segment in snake_body) or food_position == self.position:
                safe = False

            # 规则4：不在屏幕边缘（留出逃生通道）
            if (self.x < snake_block * 2 or self.x > display_width - snake_block * 3 or
                    self.y < snake_block * 2 or self.y > display_height - snake_block * 3):
                safe = False

            if safe:
                return

        # 如果超过最大尝试次数，允许放宽规则4
        self.x = round(random.randrange(snake_block * 2, display_width - snake_block * 3) / snake_block) * snake_block
        self.y = round(random.randrange(snake_block * 2, display_height - snake_block * 3) / snake_block) * snake_block

# 显示得分
def your_score(score):
    value = score_font.render("score: " + str(score), True, black)
    dis.blit(value, [0, 0])

# 显示游戏时间
def display_game_time(game_time):
    time_text = score_font.render("Time: " + str(int(game_time)) + "s", True, black)  # 使用与得分一致的字体
    time_rect = time_text.get_rect(topright=(display_width - 10, 10))  # 距离右上角各10像素
    dis.blit(time_text, time_rect)


# 显示消息
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [display_width / 6, display_height / 3])

# 绘制开始按钮
def draw_start_button(mouse_pos=None):
    button_rect = pygame.Rect(display_width // 2 - 100, display_height // 2 + 100, 200, 60)

    # 检查鼠标是否悬停在按钮上
    if mouse_pos and button_rect.collidepoint(mouse_pos):
        button_color = (255, 215, 0)  # 悬停时颜色变亮
        border_color = (0, 0, 200)  # 边框颜色变深
    else:
        button_color = yellow  # 默认颜色
        border_color = black  # 默认边框颜色

    pygame.draw.rect(dis, button_color, button_rect, border_radius=10)
    pygame.draw.rect(dis, border_color, button_rect, 2, border_radius=10)

    button_text = button_font.render("START", True, black)  # 文字改为"START"
    text_rect = button_text.get_rect(center=button_rect.center)
    dis.blit(button_text, text_rect)

    return button_rect

# 显示开始页面
def show_start_screen():
    waiting = True
    start_sound.play()  # 播放开始界面音效
    while waiting:
        mouse_pos = pygame.mouse.get_pos()  # 获取鼠标位置
        dis.fill(white)
        dis.blit(background1, (0, 0))

        # 绘制游戏标题
        title_text = font_title.render("爱吃樱花的珞珈小蛇", True, red)
        title_rect = title_text.get_rect(center=(display_width // 2, display_height // 2 - 50))
        dis.blit(title_text, title_rect)

        # 绘制提示信息
        hint_text = font_style.render("Press S or click the button to start the game.", True, black)
        hint_rect = hint_text.get_rect(center=(display_width // 2, display_height // 2 + 40))
        dis.blit(hint_text, hint_rect)

        # 绘制开始按钮（传递鼠标位置）
        button_rect = draw_start_button(mouse_pos)

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    button_click_sound.play()  # 播放按钮点击音效
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    button_click_sound.play()  # 播放按钮点击音效
                    pygame.time.delay(400)  # 添加短暂延迟让音效播放完整
                    return

        pygame.display.update()
        clock.tick(15)

# 初始化游戏
def init_game():
    startX = (display_width // 2 // snake_block) * snake_block
    startY = (display_height // 2 // snake_block) * snake_block
    snake = Snake(float(startX), float(startY))
    obstacles = []
    for i in range(5):  # 创建5个障碍物
        obstacle = Obstacle()
        obstacles.append(obstacle)
    food = Food()
    food.respawn([obstacle for obstacle in obstacles], snake.body)
    current_ticks = pygame.time.get_ticks()
    return snake, obstacles, food, pygame.time.get_ticks(), 0, 0, current_ticks

game_active = True

# 定义游戏结束界面
def end_game(final_score, final_time):
    pygame.mixer.music.stop()  # 停止主体背景音乐
    pygame.mixer.stop()  # 确保之前的音效都停止
    game_over_sound.play()  # 播放游戏结束部分音效
    while True:
        dis.fill(white)
        dis.blit(background3, (0, 0))

        game_font_over = pygame.font.Font(font_name, 50)
        game_font_restart = pygame.font.Font(font_name, 30)
        game_message_over = game_font_over.render("GAME OVER", True, red)
        game_message_over_rect = game_message_over.get_rect(center=(display_width//2, display_height//2-100))
        dis.blit(game_message_over, game_message_over_rect)

        game_message_restart = game_font_restart.render("Press RESTART or QUIT", True, (64, 64, 64))
        game_message_restart_rect = game_message_restart.get_rect(center=(display_width//2, display_height//2-50))
        dis.blit(game_message_restart, game_message_restart_rect)

        # 显示得分和时间
        your_score(final_score)
        display_game_time(final_time)

        # 按钮
        restart_btn = pygame.Rect(display_width // 2 - 150, 550, 100, 40)
        quit_btn = pygame.Rect(display_width // 2 + 50, 550, 100, 40)

        pygame.draw.rect(dis, yellow, restart_btn, border_radius=10)
        pygame.draw.rect(dis, yellow, quit_btn, border_radius=10)

        restart_text = font_style.render("RESTART", True, black)
        quit_text = font_style.render("QUIT", True, black)

        dis.blit(restart_text, restart_text.get_rect(center=restart_btn.center))
        dis.blit(quit_text, quit_text.get_rect(center=quit_btn.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(event.pos):
                    button_click_sound.play()  # 播放按钮点击音效
                    pygame.time.delay(400)  # 添加短暂延迟让音效播放完整
                    return "restart"
                elif quit_btn.collidepoint(event.pos):
                    button_click_sound.play()  # 播放按钮点击音效
                    pygame.time.delay(400)  # 添加短暂延迟让音效播放完整
                    return "quit"

        pygame.display.update()
        clock.tick(15)


# 主游戏流程
def main():
    global game_active
    final_score = 0
    final_time = 0
    # 显示开始页面
    show_start_screen()

    # 初始化游戏
    snake, obstacles, food, start_ticks, final_score, final_time, last_obstacle_refresh = init_game()

    # 开始播放背景音乐
    if background_music:
        pygame.mixer.music.load(background_music)
        pygame.mixer.music.play(-1)

    last_obstacle_refresh = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()

        if current_time - last_obstacle_refresh > 10000:
            snake_head = snake.body[-1]
            snake_dir = snake.current_direction()
            for obstacle in obstacles:
                obstacle.respawn(
                    snake_head=snake_head,
                    snake_direction=snake_dir,
                    obstacles=obstacles,
                    snake_body=snake.body,
                    food_position=[food.x, food.y]
                )
            last_obstacle_refresh = current_time
            # 添加刷新提示
            pygame.mixer.Sound.play(button_click_sound)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if game_active == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        snake.change_direction("LEFT")
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction("RIGHT")
                    elif event.key == pygame.K_UP:
                        snake.change_direction("UP")
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction("DOWN")
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # 重置游戏
                        snake.reset()
                        food.respawn(obstacles, snake.body)
                        game_active = True
                        start_ticks = pygame.time.get_ticks()
                        final_score = 0
                        final_time = 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # 检查是否点击了"按空格键重新开始"的区域
                    if display_width // 6 <= event.pos[0] <= display_width * 5 // 6 and \
                            display_height // 3 <= event.pos[1] <= display_height // 3 + 30:
                        snake.reset()
                        food.respawn(obstacles, snake.body)
                        game_active = True
                        start_ticks = pygame.time.get_ticks()
                        final_score = 0
                        final_time = 0

        # 游戏逻辑
        if game_active:
            # 蛇移动
            snake.move()

            # 清空屏幕,绘制背景图
            dis.fill(white)
            dis.blit(background2, (0, 0))
            # dis.blit(overlay, (0, 0))

            # 绘制食物
            food.draw()

            # 绘制障碍物
            for obstacle in obstacles:
                obstacle.draw()

            # 绘制蛇和显示得分
            snake.draw()
            current_score = snake.length - 3
            your_score(current_score)

            # 显示游戏时间
            seconds_elapsed = (pygame.time.get_ticks() - start_ticks) / 1000
            display_game_time(seconds_elapsed)

            # 检查是否吃到食物
            if snake.check_collision_with_food(food):
                eat_sound.play()

                # 根据食物类型计算增长长度
                if food.is_big_reward:
                    growth = food.big_reward_multiplier  # 大奖励增长3节

                else:
                    growth = 1  # 普通食物增长1节

                for _ in range(growth):
                    snake.grow()

                # 生成新食物时传入当前分数
                food.respawn(obstacles, snake.body, current_score + growth)  # +growth因为分数即将增加
            # collision_result = snake.check_collision_with_food(food)  # 先保存结果
            # if collision_result:  # 使用保存的结果
            #    print("调试: 检测到碰撞!")  # 确认此行是否执行
            #    eat_sound.play()  # 播放吃食物音效
            # 生成新的食物位置
            #    food.respawn([obstacle for obstacle in obstacles], snake.body)
            # 蛇增长
            #    snake.grow()

            # 检查是否撞到自己
            if snake.check_collision_with_self():
                crash_sound.play()  # 播放碰撞音效
                game_active = False
                final_score = current_score
                final_time = seconds_elapsed

            # 检查是否撞到边界
            # if snake.check_collision_with_boundaries():
            #     crash_sound.play()  # 播放碰撞音效
            #     game_active = False
            #     final_score = current_score
            #     final_time = seconds_elapsed

            # 检查是否撞到障碍物
            for obstacle in obstacles:
                if snake.check_collision_with_obstacle(obstacle):
                    crash_sound.play()  # 播放碰撞音效
                    game_active = False
                    final_score = current_score
                    final_time = seconds_elapsed

        else:
            action = end_game(final_score, final_time)
            if action == "restart":
                snake, obstacles, food, start_ticks, final_score, final_time, last_obstacle_refresh = init_game()
                game_active = True
                if background_music:
                    pygame.mixer.music.play(-1)
            elif action == "quit":
                pygame.quit()
                exit()

            your_score(final_score)
            display_game_time(final_time)

        pygame.display.update()
        clock.tick(snake_speed)


if __name__ == "__main__":
    main()