# 全局配置常量

# 屏幕
SCREEN_SIZE = (1080, 720)  # 窗口尺寸
FPS = 60                   # 帧率上限

# 玩家
RADIUS = 10         # 玩家半径
SPEED_FAST = 300    # 正常移动速度 (像素/秒)
SPEED_SLOW = 100    # 按住 Shift 时的减速
BLINK_DIST = 75     # 闪烁距离 (像素)
BLINK_CD = 0.6      # 闪烁冷却时间 (秒)
TRAIL_LIFE = 0.35   # 拖影持续时间 (秒)

# 弹幕
BULLET_RADIUS = 6              # 弹幕半径
BULLET_SPEED = (150, 320)      # 弹幕速度范围
SPAWN_INTERVAL = (0.4, 0.9)    # 弹幕生成间隔范围 (秒)
SPAWN_COUNT = (1, 3)           # 每波弹幕数量范围
SPAWN_DELAY = 0.8              # 开局/重开后首次生成弹幕的延迟 (秒)
CULL_MARGIN = 60               # 弹幕飞出屏幕多远后移除

# 子弹 (玩家发射)
SHOT_RADIUS = 4       # 子弹半径
SHOT_SPEED = 500      # 子弹速度 (像素/秒)
FIRE_CD = 0.25        # 开火冷却时间 (秒)

# 消散粒子
PARTICLE_LIFE = 0.7   # 消散粒子持续时间 (秒)
PARTICLE_COUNT = 36   # 消散粒子数量

# 颜色
PLAYER_FILL = (255, 255, 255)
PLAYER_BORDER = (0, 0, 255)
BULLET_COLOR = (255, 0, 0)
SHOT_COLOR = (80, 255, 80)
TRAIL_COLOR = (150, 180, 255)
PARTICLE_COLORS = ((255, 255, 255), (100, 140, 255))
