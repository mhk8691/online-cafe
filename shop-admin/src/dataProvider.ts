import simpleRestProvider from "ra-data-simple-rest";

export const dataProvider = simpleRestProvider(
  import.meta.env.VITE_SIMPLE_REST_URL
);


// import { withLifecycleCallbacks, DataProvider } from "react-admin";

// const dataProvider = withLifecycleCallbacks(
//   simpleRestProvider("http://localhost:5173/product"),
//   [
//     {
//       /**
//        * For posts update only, convert uploaded images to base 64 and attach them to
//        * the `picture` sent property, with `src` and `title` attributes.
//        */
//       resource: "ProductCreate",
//       beforeUpdate: async (params: any, dataProvider: DataProvider) => {
//         // Freshly dropped pictures are File objects and must be converted to base64 strings
//         const newPictures = params.data.pictures.filter(
//           (p: { rawFile: any; }) => p.rawFile instanceof File
//         );
//         const formerPictures = params.data.pictures.filter(
//           (p: { rawFile: any; }) => !(p.rawFile instanceof File)
//         );

//         const base64Pictures = await Promise.all(
//           newPictures.map(convertFileToBase64)
//         );

//         const pictures = [
//           ...base64Pictures.map((dataUrl, index) => ({
//             src: dataUrl,
//             title: newPictures[index].title,
//           })),
//           ...formerPictures,
//         ];

//         return {
//           ...params,
//           data: {
//             ...params.data,
//             pictures,
//           },
//         };
//       },
//     },
//   ]
// );

// /**
//  * Convert a `File` object returned by the upload input into a base 64 string.
//  * That's not the most optimized way to store images in production, but it's
//  * enough to illustrate the idea of dataprovider decoration.
//  */
// const convertFileToBase64 = (file: { rawFile: Blob; }) =>
//   new Promise((resolve, reject) => {
//     const reader = new FileReader();
//     reader.onload = () => resolve(reader.result);
//     reader.onerror = reject;
//     reader.readAsDataURL(file.rawFile);
//   });

// export default dataProvider;