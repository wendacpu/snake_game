import pygame

# 初始化pygame
pygame.init()

# 定义颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
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


# 显示得分
def your_score(score):
    value = score_font.render("得分: " + str(score), True, black)
    dis.blit(value, [0, 0])


# 绘制蛇
def our_snake(snake_block, snake_list):
    # 绘制蛇头（不同颜色）
    if len(snake_list) > 0:
        head = snake_list[-1]
        pygame.draw.rect(dis, blue, [head[0], head[1], snake_block, snake_block])

    # 绘制蛇身
    for x in snake_list[:-1]:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])


# 绘制障碍物
def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(dis, gray, [obstacle[0], obstacle[1], snake_block, snake_block])


# 显示消息
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [display_width / 6, display_height / 3])


# 游戏主循环
def gameLoop():
    game_over = False
    game_close = False

    # 初始化蛇的位置
    x1 = display_width / 2
    y1 = display_height / 2

    # 初始化蛇的移动方向（默认向右移动）
    x1_change = snake_block
    y1_change = 0

    # 初始化蛇的身体
    snake_List = []
    Length_of_snake = 3  # 初始长度设为3，更容易看到

    # 创建障碍物
    obstacles = []
    for i in range(5):  # 创建5个障碍物
        obstacle_x = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
        obstacle_y = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block
        obstacles.append([obstacle_x, obstacle_y])

    # 随机生成食物位置（确保不在障碍物上）
    foodx = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block

    # 确保食物不在障碍物上
    while [foodx, foody] in obstacles:
        foodx = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
        foody = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block

    while not game_over:

        while game_close == True:
            dis.fill(white)
            message("游戏结束! 按Q退出或按C重新开始", red)
            your_score(Length_of_snake - 1)
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
                if event.key == pygame.K_LEFT and x1_change != snake_block:  # 防止直接反向移动
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change != -snake_block:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change != snake_block:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change != -snake_block:
                    y1_change = snake_block
                    x1_change = 0

        # 检查是否撞到边界
        if x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0:
            game_close = True

        # 更新蛇的位置
        x1 += x1_change
        y1 += y1_change
        dis.fill(white)

        # 绘制食物
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])

        # 绘制障碍物
        draw_obstacles(obstacles)

        # 更新蛇的身体
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        # 如果蛇的长度超过了应有的长度，删除多余的部分
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # 检查是否撞到自己
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # 检查是否撞到障碍物
        for obstacle in obstacles:
            if snake_Head == obstacle:
                game_close = True

        # 绘制蛇和显示得分
        our_snake(snake_block, snake_List)
        your_score(Length_of_snake - 1)

        pygame.display.update()

        # 检查是否吃到食物
        if x1 == foodx and y1 == foody:
            # 生成新的食物位置
            foodx = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block

            # 确保食物不在障碍物上和蛇身上
            while [foodx, foody] in obstacles or [foodx, foody] in snake_List:
                foodx = round(random.randrange(0, display_width - snake_block) / snake_block) * snake_block
                foody = round(random.randrange(0, display_height - snake_block) / snake_block) * snake_block

            Length_of_snake += 1

        # 控制游戏速度
        clock.tick(snake_speed)

    # 退出pygame
    pygame.quit()
    quit()


# 启动游戏
gameLoop()