<template>
  <div id="container">
    <div id="text_welcome">Welcome Hoang Nam</div>
    <div>
      <table class="table table-responsive table-bordered" id="table_1">
        <tr>
          <th>
            #
          </th>
          <th>
            Widget Title
          </th>
          <th>
            Widget Description
          </th>
          <th>
            Product included
          </th>
          <th>
            Total Price
          </th>
          <td>
            Status
          </td>
        </tr>
        <tr>
          <td>
            1
          </td>
          <td>
            You May Also Like...
          </td>
          <td>
            Good deals only for you!
          </td>
          <td>
            3
          </td>
          <td>
            $100.05
          </td>
          <td>
            <div id="switch">
              <div class="form-check form-switch">
                <input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault">
                <label class="form-check-label" for="flexSwitchCheckDefault"></label>
              </div>
            </div>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: "Dashboard"
}
</script>

<style scoped>
#container {
  padding: 57px;
  width: 100%;
}

#text_welcome {
  padding: 20px 20px 20px 20px;
  width: 500px;
  height: 100px;
  left: 20px;
  top: 5px;
  font-family: 'Kanit';
  font-style: normal;
  font-weight: 600;
  font-size: 27px;
  line-height: 24px;
  color: #000000;
}

#table_1 {
  display: table;
  width: 100%;
  left: 20px;
  top: 5px;
  column-gap: 30px;
  row-gap: 30px;
}


#table_1 th {
  text-align: left !important;
}

#table_1 td {
  text-align: left;
  font-family: 'Inter';
  font-style: normal;
  color: rgba(0, 0, 0, 0.85);
  flex: none;
  order: 0;
  flex-grow: 0;

}
</style>