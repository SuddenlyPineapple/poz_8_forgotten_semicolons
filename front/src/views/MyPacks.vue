<template>
    <div>
        <v-container>
            <v-layout row>
                 <v-flex xs12>
                     <h1 class="mb-3 gray--text">Twoje Paczki</h1>
                    <PackagesTable></PackagesTable>
                </v-flex>
            </v-layout>
        </v-container>
    </div>
</template>

<script lang="ts">
import {Vue, Component, Prop} from 'vue-property-decorator';
import PackagesTable from '../components/PackagesTable.vue';

@Component({
    components: {
        PackagesTable,
    }
})
export default class MyPacks extends Vue {

}

</script>

<style lang="scss">

</style>