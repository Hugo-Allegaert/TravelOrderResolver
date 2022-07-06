<template>
    <div>
        <div class="section-header" v-on:click="expand = !expand">
            <h2>{{title}}</h2>
            <span style="transition: all 0.2s linear" v-bind:class="{rotate: expand}">
                <i class="fa fa-chevron-down"></i>
            </span>
        </div>
        <div v-if="expand == true">
            <slot></slot>
        </div>
    </div>
</template>

<script lang="ts">
export default {
    name: 'Collapsable',
    props: {
        title: String,
        collapse: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            expand: this.collapse
        }
    } 
}
</script>

<style scoped>

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.2s linear;
    cursor: pointer;
}

.rotate {
    transform: rotate(180deg);
}

</style>