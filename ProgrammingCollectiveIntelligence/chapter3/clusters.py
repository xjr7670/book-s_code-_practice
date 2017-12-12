from math import sqrt
from PIL import Image, ImageDraw


def readfile(filename):
    lines = [line for line in open(filename)]

    # 第一行是列标题
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        # 每行的第一列是行名
        rownames.append(p[0])
        # 剩余部分就是该行对应的数据
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data

def pearson(v1, v2):
    # 简单求和
    sum1 = sum(v1)
    sum2 = sum(v2)

    # 求平方和
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    # 求乘积之和
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    # 计算r (Pearson socre)
    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)))
    if den == 0:
        return 0
    return 1.0 - num / den

class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.distance = distance
        self.id = id

def hcluster(rows, distance=pearson):
    distances = {}
    currentclustid = -1

    # 最开始的聚类就是数据集中的行
    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]

    while len(clust) > 1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

        # 遍历每一个配对，寻找最小距离
        for i in range(len(clust)):
            for j in range(i+1, len(clust)):
                # 用distances来缓存距离的计算值
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)

                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowestpair = (i, j)
        # 计算两个聚类的平均值
        mergevec = [
        (clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0 \
        for i in range(len(clust[0].vec))
        ]

        # 建立新的聚类
        newcluster = bicluster(mergevec, left=clust[lowestpair[0]], 
            right=clust[lowestpair[1]], 
            distance=closest, id=currentclustid)

        # 不在原始集合中的聚类，其id为负数
        currentclustid -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]

def printclust(clust, labels=None, n=0):
    # 利用缩进来建立层级布局
    for i in range(n):
        print(' ')
    if clust.id < 0:
        # 负数标记代表这是一个分支
        print('-')
    else:
        # 正数标记代表这是一个叶节点
        if labels == None:
            print(clust.id)
        else:
            print(labels[clust.id])

    # 现在开始打印右侧分支和左侧分支
    if clust.left != None:
        printclust(clust.left, labels=labels, n=n+1)
    if clust.right != None:
        printclust(clust.right, labels=labels, n=n+1)

def getheight(clust):
    # 这是一个叶节点吗？如果是则高度为1
    if clust.left == None and clust.right == None:
        return 1

    # 否则，高度为每个分支的高度这和
    return getheight(clust.left) + getheight(clust.right)

def getdepth(clust):
    # 一个叶节点的距离是0.0
    if clust.left == None and clust.right == None:
        return 0

    # 一个枝节点的距离等于左右两侧分支中距离较大者
    # 加上该枝节点自身的距离
    return max(getdepth(clust.left), getdepth(clust.right)) + clust.distance

def drawdendrogram(clust, labels, jpeg='clusters.jpg'):
    # 高度和宽度
    h = getheight(clust) * 20
    w = 1200
    depth = getdepth(clust)

    # 由于宽度是固定的，因此我们需要对距离值做相应的调整
    scaling = float(w - 150) / depth

    # 新建一个白色背景的图片
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, h/2, 10, h/2), fill=(255, 0, 0))

    # 画第一个节点
    drawnode(draw, clust, 10, (h/2), scaling, labels)
    img.save(jpeg, 'JPEG')

def drawnode(draw, clust, x, y, scaling, labels):
    if clust.id < 0:
        h1 = getheight(clust.left) * 20
        h2 = gethieght(clust.right) * 20
        top = y - (h1 + h2) / 2
        bottom = y + (h1 + h2) / 2
        # 线的长度
        l1 = clust.distance * scaling
        # 聚类到其子节点的垂直线
        draw.line((x, top+h1/2, x, bottom-h2/2), fill=(255, 0, 0))

        # 连接左侧节点的水平线
        draw.line((x, top+h1/2, x+l1, top+h1/2), fill=(255, 0, 0))

        # 连接右侧节点的水平线
        draw.line((x, bottom-h2/2, x+l1, bottom-h2/2), fill=(255, 0, 0))

        # 调用函数绘制左右节点
        drawnode(draw, clust.left, x+l1, top+h1/2, scaling, labels)
        drawnode(draw, clust.right, x+l1, bottom-h2/2, scaling, labels)
    else:
        # 如果这是一个叶节点，则绘制节点的标签
        draw.text((x+5, y-7), labels[clust.id], (0, 0, 0))
