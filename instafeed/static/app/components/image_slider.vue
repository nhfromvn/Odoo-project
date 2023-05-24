<template>
  <div class="image-slider">
    <div class="slides">
      <div class="slide" :style="{display: 'grid',
                                            gap: gap.value+'px',
                                            gridTemplateColumns:'repeat('+per_slide+',1fr)'
                                            }">

        <template v-for="image in chunkedImages[currentSlide]">
          <div :style="{aspectRatio:ratio,position:'relative'}" @mouseenter="image.hover=true"
               @mouseleave="image.hover=false">
            <img v-if="image.type=='IMAGE'" style="width: 100%;
                        object-fit: fill;
                    height: 100%" :src="image.media_url" :alt="image.caption"/>
            <img v-if="image.type=='VIDEO'" :style="{
                                    width: '100%',
                                    height: '100%'
                        }" :src="image.thumbnail_url" :alt="image.caption">
            <div class="post_hover" v-if="image.hover&&image.type=='IMAGE'" @click="show_post(image)">
              <font-awesome-icon icon="fa-brands fa-instagram"
                                 style="color: white; height: 15%; width: 15%"/>
            </div>
            <div class="post_hover" v-if="image.hover&&image.type=='VIDEO'" @click="show_post(image)">
              <font-awesome-icon icon="fa-solid fa-play"
                                 style="color: white; height: 15%; width: 15%"/>
            </div>
          </div>
        </template>
      </div>
      <div class="slide_controls">
        <font-awesome-icon @click="prevSlide" :icon="['fas', 'circle-chevron-left']"/>
        <font-awesome-icon @click="nextSlide" :icon="['fas', 'circle-chevron-right']"/>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  props: {
    images: {
      type: Array,
      required: true,
    },
    per_slide: Number,
    gap: Object,
    ratio: Number,
  },
  data() {
    return {
      currentSlide: 0,
    };
  }, watch: {
    images: function () {
      if (this.images.length <= this.per_slide) {
        this.currentSlide = 0
      }
    },
    per_slide: function () {
      if (this.currentSlide > this.images.length / this.per_slide-1) {
        this.currentSlide = 0
      }
    }
  },
  computed: {
    chunkedImages() {
      const chunks = [];
      if (this.per_slide > 0) {
        for (let i = 0; i < this.images.length; i += this.per_slide) {
          chunks.push(this.images.slice(i, i + this.per_slide));
        }
      }
      return chunks;
    },
  },
  methods: {
    show_post(post) {
      this.$emit('show_post', post)
    },
    prevSlide() {
      this.currentSlide =
          this.currentSlide <= 0 ? this.chunkedImages.length - 1 : this.currentSlide - 1;
      console.log(this.currentSlide)
    },
    nextSlide() {
      this.currentSlide =
          this.currentSlide >= this.chunkedImages.length - 1 ? 0 : this.currentSlide + 1;
      console.log(this.currentSlide)
    },
  },
};
</script>

<style scoped>
.image-slider {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.slides {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: hidden;
  width: 100%;
  position: relative;
}

.slide {
  width: 100%;
}

img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.slide_controls {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
  top: 50%;
  transform: translate(-0%, -50%);
  margin-top: auto;
  position: absolute;
  z-index: 99;
}

.slide_controls svg {
  font-size: 30px;
}

.post_hover {
  width: 100%;
  height: 100%;
  cursor: pointer;
  display: flex;
  text-align: center;
  align-items: center;
  justify-content: center;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 20;
  position: absolute;
  opacity: 0.5;
  background: #151515
}

.fa-circle-chevron-right {
  color: #949494;
}

.fa-circle-chevron-left {
  color: #949494;
}
</style>