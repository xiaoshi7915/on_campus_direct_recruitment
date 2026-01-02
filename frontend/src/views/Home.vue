<template>
  <div class="home flex flex-col w-full flex-1 min-h-0">
    <!-- 图片显示区域 - 填满整个可用空间 -->
    <div class="w-full h-full flex items-center justify-center overflow-hidden">
      <img 
        ref="heroImage"
        :src="heroImageSrc" 
        alt="校园直聘平台" 
        class="w-full h-full object-cover"
        style="display: block !important; visibility: visible !important; opacity: 1 !important;"
        @error="handleImageError"
        @load="handleImageLoad"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

const heroImage = ref<HTMLImageElement | null>(null)
const heroImageSrc = ref('/images/hero.png')

// #region agent log
console.log('[DEBUG A] heroImage ref initialized', { heroImageValue: heroImage.value, heroImageSrc: heroImageSrc.value })
// #endregion


// 处理图片加载错误
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  console.error('图片加载失败:', img.src, '错误:', event)
  // 如果 hero.png 加载失败，回退到 background.jpg
  if (img.src.includes('hero.png')) {
    console.log('回退到 background.jpg')
    img.src = '/images/background.jpg'
  }
}

// 图片加载成功回调
const handleImageLoad = (event: Event) => {
  const img = event.target as HTMLImageElement
  // #region agent log
  console.log('[DEBUG D] handleImageLoad called', {
    src: img.src,
    naturalWidth: img.naturalWidth,
    naturalHeight: img.naturalHeight,
    refValue: heroImage.value === img,
    isRefBound: !!heroImage.value
  })
  // #endregion
  console.log('图片加载成功:', {
    src: img.src,
    naturalWidth: img.naturalWidth,
    naturalHeight: img.naturalHeight,
    width: img.width,
    height: img.height,
    offsetWidth: img.offsetWidth,
    offsetHeight: img.offsetHeight,
    clientWidth: img.clientWidth,
    clientHeight: img.clientHeight,
    scrollWidth: img.scrollWidth,
    scrollHeight: img.scrollHeight,
    style: {
      display: img.style.display,
      visibility: img.style.visibility,
      opacity: img.style.opacity,
      width: img.style.width,
      height: img.style.height
    },
    computedStyle: {
      display: window.getComputedStyle(img).display,
      visibility: window.getComputedStyle(img).visibility,
      opacity: window.getComputedStyle(img).opacity,
      width: window.getComputedStyle(img).width,
      height: window.getComputedStyle(img).height,
      position: window.getComputedStyle(img).position,
      zIndex: window.getComputedStyle(img).zIndex
    },
    parentElement: img.parentElement?.tagName,
    parentStyle: img.parentElement ? {
      display: window.getComputedStyle(img.parentElement).display,
      overflow: window.getComputedStyle(img.parentElement).overflow,
      width: window.getComputedStyle(img.parentElement).width,
      height: window.getComputedStyle(img.parentElement).height
    } : null
  })
  
  // 如果图片尺寸为0，尝试强制设置尺寸
  if (img.naturalWidth > 0 && img.naturalHeight > 0 && (img.offsetWidth === 0 || img.offsetHeight === 0)) {
    console.warn('图片尺寸为0，尝试修复...')
    const aspectRatio = img.naturalWidth / img.naturalHeight
    const maxHeight = 550
    const calculatedWidth = maxHeight * aspectRatio
    img.style.width = `${calculatedWidth}px`
    img.style.height = `${maxHeight}px`
    console.log('已设置图片尺寸:', { width: calculatedWidth, height: maxHeight })
  }
}

onMounted(() => {
  // #region agent log
  console.log('[DEBUG A] onMounted called', { heroImageValue: heroImage.value, heroImageSrc: heroImageSrc.value })
  // #endregion
  
  // 立即检查
  // #region agent log
  const immediateCheck = heroImage.value;
  console.log('[DEBUG A] immediate ref check in onMounted', { heroImageValue: immediateCheck, hasRef: !!immediateCheck, refType: immediateCheck?.constructor?.name })
  // #endregion
  
  // 使用 nextTick 检查
  nextTick(() => {
    // #region agent log
    const nextTickCheck = heroImage.value;
    console.log('[DEBUG C] nextTick ref check', { 
      heroImageValue: nextTickCheck, 
      hasRef: !!nextTickCheck, 
      refType: nextTickCheck?.constructor?.name,
      parentElement: nextTickCheck?.parentElement?.tagName,
      allImages: document.querySelectorAll('img').length,
      imagesWithAlt: Array.from(document.querySelectorAll('img')).map(i => ({ alt: i.alt, src: i.src }))
    })
    // #endregion
    
    if (nextTickCheck) {
      // #region agent log
      const computedStyle = window.getComputedStyle(nextTickCheck);
      console.log('[DEBUG D] nextTick image state', {
        complete: nextTickCheck.complete,
        naturalWidth: nextTickCheck.naturalWidth,
        naturalHeight: nextTickCheck.naturalHeight,
        offsetWidth: nextTickCheck.offsetWidth,
        offsetHeight: nextTickCheck.offsetHeight,
        src: nextTickCheck.src,
        display: computedStyle.display,
        visibility: computedStyle.visibility,
        opacity: computedStyle.opacity
      })
      // #endregion
    } else {
      // #region agent log
      const querySelectorImg = document.querySelector('img[alt="校园直聘平台"]');
      const allImages = document.querySelectorAll('img');
      console.log('[DEBUG B] nextTick - image not found, querySelector fallback', {
        querySelectorResult: querySelectorImg,
        hasImgInDOM: !!querySelectorImg,
        allImagesCount: allImages.length,
        allImagesWithAlt: Array.from(allImages).map(i => ({ alt: i.alt, src: i.src, className: i.className }))
      })
      // #endregion
    }
  })
  
  // 延迟检查图片状态
  setTimeout(() => {
    const img = heroImage.value
    // #region agent log
    console.log('[DEBUG E] setTimeout 1000ms check', {
      heroImageValue: img,
      hasRef: !!img,
      refType: img?.constructor?.name,
      querySelectorResult: document.querySelector('img[alt="校园直聘平台"]')?.tagName
    })
    // #endregion
    
    if (img) {
      console.log('onMounted 检查图片状态:', {
        complete: img.complete,
        naturalWidth: img.naturalWidth,
        naturalHeight: img.naturalHeight,
        offsetWidth: img.offsetWidth,
        offsetHeight: img.offsetHeight,
        src: img.src
      })
      
      // #region agent log
      console.log('[DEBUG D] image found in setTimeout', {
        complete: img.complete,
        naturalWidth: img.naturalWidth,
        naturalHeight: img.naturalHeight,
        offsetWidth: img.offsetWidth,
        offsetHeight: img.offsetHeight,
        src: img.src
      })
      // #endregion
      
      if (!img.complete) {
        console.log('图片尚未加载完成，等待加载事件...')
      } else if (img.naturalWidth === 0) {
        console.error('图片加载失败或无效')
      } else {
        console.log('图片已加载，但可能不可见')
      }
    } else {
      console.error('图片元素未找到')
      // #region agent log
      const querySelectorImg = document.querySelector('img[alt="校园直聘平台"]');
      const allImages = document.querySelectorAll('img');
      console.log('[DEBUG B] image not found - querySelector fallback', {
        querySelectorResult: querySelectorImg,
        hasImgInDOM: !!querySelectorImg,
        allImagesCount: allImages.length,
        allImagesWithAlt: Array.from(allImages).map(i => ({ alt: i.alt, src: i.src, className: i.className }))
      })
      // #endregion
    }
  }, 1000)
})

onUnmounted(() => {
  // Cleanup if needed
})
</script>

<style scoped>
.home {
  position: relative;
  overflow: visible;
}

.home::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(79, 70, 229, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

.home::after {
  content: '';
  position: absolute;
  bottom: -30%;
  left: -10%;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(236, 72, 153, 0.08) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}
</style>
