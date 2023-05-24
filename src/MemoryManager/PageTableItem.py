class PageTableItem:
    page_num = 0 #0级页表
    # page1_num = 0 #1级页号
    out_address = 0 # 磁盘交换
    physical_block_num = 0#映射到的物理块号
    item_state = 0 #(页表项状态，0空，1已映射，2已分配但未映射到物理帧)
    write = 0 #该页的内容是否可写
    read = 0 #该页的内容是否可读
    access = 0 #访问位
    modify = 0 #修改位
    interrupt = 0 #中断位