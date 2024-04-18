// import React, { useState, useEffect } from "react";
// import axios from "axios";
// import {
//   LineChart,
//   Line,
//   XAxis,
//   YAxis,
//   CartesianGrid,
//   Tooltip,
//   Legend,
// } from "recharts";

// const Dashboard = () => {
//   const [kpis, setKpis] = useState(null);

//   useEffect(() => {
//     const fetchKpis = async () => {
//       try {
//         const response = await axios.get("http://localhost:5000/KPIs"); // Assuming this endpoint exists
//         setKpis(response.data);
//       } catch (error) {
//         console.error("Error fetching KPIs:", error);
//       }
//     };

//     fetchKpis();
//   }, []);

//   // Prepare data for the chart
//   const data = kpis
//     ? [
//         {
//           sales: kpis["total-revenue"],
//         },
//         // Add more data points for additional weeks if available
//       ]
//     : [];

//   return (
//     <div>
//       <h1>Admin Dashboard</h1>
//       {kpis && (
//         <div>
//           <h2>Total Revenue: {kpis["total-revenue"]}</h2>
//           <h2>Total Orders: {kpis["total-orders"]}</h2>
//           <h2>Charts:</h2>
//           <LineChart width={800} height={400} data={data}>
//             <CartesianGrid strokeDasharray="3 3" />
//             <XAxis dataKey="name" />
//             <YAxis />
//             <Tooltip />
//             <Legend />
//             <Line type="monotone" dataKey="sales" stroke="#8884d8" />
//             <Line type="monotone" dataKey="payments" stroke="#82ca9d" />
//           </LineChart>
//           {/* Add more charts as needed */}
//         </div>
//       )}
//     </div>
//   );
// };

// export default Dashboard;

// import React, { useState, useEffect } from "react";
// import axios from "axios";
// import {
//   LineChart,
//   Line,
//   XAxis,
//   YAxis,
//   CartesianGrid,
//   Tooltip,
//   Legend,
// } from "recharts";

// const Dashboard = () => {
//   const [kpis, setKpis] = useState(null);

//   useEffect(() => {
//     const fetchKpis = async () => {
//       try {
//         const response = await axios.get("http://localhost:5000/KPIs"); // Assuming this endpoint exists
//         setKpis(response.data);
//       } catch (error) {
//         console.error("Error fetching KPIs:", error);
//       }
//     };

//     fetchKpis();
//   }, []);

//   return (
//     <div>
//       <h1>Admin Dashboard</h1>
//       {kpis && (
//         <div>
//           <h2>Total Revenue: {kpis["total-revenue"]}</h2>
//           <h2>Charts:</h2>
//           <LineChart width={800} height={400} data={kpis["sales_per_month"]}>
//             <CartesianGrid strokeDasharray="3 3" />
//             <XAxis dataKey="month" />
//             <YAxis />
//             <Tooltip />
//             <Legend />
//             <Line type="monotone" dataKey="sales_count" stroke="#8884d8" />
//           </LineChart>
//         </div>
//       )}
//     </div>
//   );
// };

// export default Dashboard;

import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

const Dashboard = () => {
  const [kpis, setKpis] = useState(null);

  useEffect(() => {
    const fetchKpis = async () => {
      try {
        const response = await axios.get("http://localhost:5000/KPIs"); // Assuming this endpoint exists
        setKpis(response.data);
      } catch (error) {
        console.error("Error fetching KPIs:", error);
      }
    };

    fetchKpis();
  }, []);

  return (
    <div
      style={{ display: "flex", justifyContent: "center", marginTop: "50px" }}
    >
      {kpis && (
        <div>
          <LineChart width={850} height={400} data={kpis["Orderـnumber"]}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="Orderـnumber"
              stroke="#8884d8"
              label="Sales per Month"
            />
          </LineChart>
          <LineChart width={850} height={400} data={kpis["Monthlyـsales"]}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="Monthlyـsales"
              stroke="#82ca9d"
              label="Price per Month"
            />
          </LineChart>
          <LineChart
            width={850}
            height={400}
            data={[{ name: "Total Revenue", value: kpis["total-revenue"] }]}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="value"
              stroke="#82ca9d"
              label="Total Revenue"
            />
          </LineChart>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
