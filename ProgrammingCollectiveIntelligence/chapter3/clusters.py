from PIL import Image, ImageDraw

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
