<template>
    <div class="image-slider">
        <div class="slides">
            <div class="slide" :style="{display: 'grid',
                                            gap: gap.value+'px',
                                            gridTemplateColumns:'repeat('+proptemp.per_slide+',1fr)'
                                            }">

                <template v-for="image in chunkedImages[currentSlide]">
                    <div :style="{aspectRatio:ratio}">
                        <img style="width: 100%;
                        object-fit: fill;
                    height: 100%" :src="image.url" :alt="image.alt"/>
                    </div>
                </template>
            </div>
            <div class="controls">
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
        proptemp: Object,
        gap: Object,
        ratio: Number,
    },
    data() {
        return {
            currentSlide: 0,
        };
    }, watch: {
        images: function () {
            if(this.images.length<=this.proptemp.per_slide){
                            this.currentSlide = 0
            }
        }
    },
    computed: {
        chunkedImages() {
            const chunks = [];
            for (let i = 0; i < this.images.length; i += this.proptemp.per_slide) {
                chunks.push(this.images.slice(i, i + this.proptemp.per_slide));
            }
            return chunks;
        },
    },
    methods: {
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

.controls {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 100%;
    top: 50%;
    transform: translate(-0%, -50%);
    margin-top: auto;
    position: absolute;
}

.fa-circle-chevron-right {
    color: #FFFFFF;
}

.fa-circle-chevron-left {
    color: #FFFFFF;
}
</style>