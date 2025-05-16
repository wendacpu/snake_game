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

# 设置显示窗口
display_width = 600
display_height = 400
dis = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('贪吃蛇游戏')

# 设置游戏时钟
clock = pygame.time.Clock()

# 蛇的大小和速度
snake_block = 20  # 增大蛇的大小，使其更容易看见
snake_speed = 10  # 降低速度，使游戏更容易控制

# 设置字体
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


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

    def move(self):
        # 更新蛇的位置
        self.x += self.x_change
        self.y += self.y_change

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

    def draw(self):
        # 绘制蛇头（不同颜色）
        if len(self.body) > 0:
            head = self.body[-1]
            pygame.draw.rect(dis, blue, [head[0], head[1], snake_block, snake_block])

        # 绘制蛇身
        for segment in self.body[:-1]:
            pygame.draw.rect(dis, green, [segment[0], segment[1], snake_block, snake_block])

    def check_collision_with_self(self):
        # 检查是否撞到自己
        for segment in self.body[:-1]:
            if segment == self.head:
                return True
        return False

    def check_collision_with_boundaries(self):
        # 检查是否撞到边界
        if self.x >= display_width or self.x < 0 or self.y >= display_height or self.y < 0:
            return True
        return False

    def check_collision_with_obstacle(self, obstacle):
        # 检查是否撞到障碍物
        return self.head == obstacle.position

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
        self.respawn()

    def respawn(self, obstacles=None, snake_body=None):
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

    def draw(self):
        # 绘制食物
        pygame.draw.rect(dis, red, [self.x, self.y, snake_block, snake_block])


# 障碍物类
class Obstacle:
    def __init__(self, x=None, y=None):
        if x is None or y is None:
            self.x = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
            self.y = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
        else:
            self.x = x
            self.y = y
        self.position = [self.x, self.y]

    def draw(self):
        # 绘制障碍物
        pygame.draw.rect(dis, gray, [self.x, self.y, snake_block, snake_block])


# 显示得分
def your_score(score):
    value = score_font.render("得分: " + str(score), True, black)
    dis.blit(value, [0, 0])


# 显示游戏时间
def display_game_time(game_time):
    time_text = score_font.render("Time: " + str(int(game_time)) + "s", True, black)  # 使用与得分一致的字体
    # 将时间显示在屏幕右上角，您可以根据需要调整位置 [display_width - 150, 0]
    time_rect = time_text.get_rect(topright=(display_width - 10, 10))  # 距离右上角各10像素
    dis.blit(time_text, time_rect)


# 显示消息
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [display_width / 6, display_height / 3])


# 游戏主循环
def gameLoop():
    game_over = False
    game_close = False

    start_ticks = pygame.time.get_ticks()

    # 初始化蛇
    snake = Snake(display_width / 2, display_height / 2)

    # 创建障碍物
    obstacles = []
    for i in range(5):  # 创建5个障碍物
        obstacle = Obstacle()
        obstacles.append(obstacle)

    # 创建食物
    food = Food()
    # 确保食物不在障碍物上
    food.respawn([obstacle for obstacle in obstacles], snake.body)

    while not game_over:

        while game_close == True:
            dis.fill(white)
            message("游戏结束! 按Q退出或按C重新开始", red)
            your_score(snake.length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")
                elif event.key == pygame.K_UP:
                    snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")

        # 检查是否撞到边界
        if snake.check_collision_with_boundaries():
            game_close = True

        # 移动蛇
        snake.move()

        # 清空屏幕
        dis.fill(white)

        # 绘制食物
        food.draw()

        # 绘制障碍物
        for obstacle in obstacles:
            obstacle.draw()

        # 检查是否撞到自己
        if snake.check_collision_with_self():
            game_close = True

        # 检查是否撞到障碍物
        for obstacle in obstacles:
            if snake.check_collision_with_obstacle(obstacle):
                game_close = True

        # 绘制蛇和显示得分
        snake.draw()
        your_score(snake.length - 1)

        # 显示游戏时间
        seconds_elapsed = (pygame.time.get_ticks() - start_ticks) / 1000  # 转换为秒
        display_game_time(seconds_elapsed)

        pygame.display.update()

        # 检查是否吃到食物
        if snake.check_collision_with_food(food):
            # 生成新的食物位置
            food.respawn([obstacle for obstacle in obstacles], snake.body)
            # 蛇增长
            snake.grow()

        # 控制游戏速度
        clock.tick(snake_speed)

    # 退出pygame
    pygame.quit()
    quit()


# 启动游戏
gameLoop()